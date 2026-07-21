"""Run the FMCG customer segmentation and purchase-driver analysis."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    RocCurveDisplay,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    silhouette_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RANDOM_SEED = 42
ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / "03_Data" / "raw" / "fmcg_consumer_survey_synthetic.csv"
PROCESSED_DATA = ROOT / "03_Data" / "processed" / "fmcg_consumer_scored.csv"
FIGURE_DIR = ROOT / "04_Output" / "figures"
TABLE_DIR = ROOT / "04_Output" / "tables"

CONSTRUCTS = [
    "price_sensitivity", "quality_orientation", "health_orientation",
    "sustainability_orientation", "digital_influence",
    "convenience_orientation", "brand_trust", "new_product_intention",
]
SEGMENTATION_FEATURES = CONSTRUCTS[:-1] + ["promotion_response"]
SEGMENT_ORDER = [
    "Value Seekers", "Digital Trend Explorers", "Convenience Loyalists",
    "Quality & Wellness Enthusiasts",
]


def cronbach_alpha(items: pd.DataFrame) -> float:
    items = items.astype(float)
    k = items.shape[1]
    return float(k / (k - 1) * (1 - items.var(ddof=1).sum() / items.sum(axis=1).var(ddof=1)))


def construct_scale_scores(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    reliability_rows = []
    scored = data.copy()
    for construct in CONSTRUCTS:
        cols = [f"{construct}_{item}" for item in range(1, 4)]
        scored[cols] = scored[cols].apply(lambda s: s.fillna(s.median()))
        scored[construct] = scored[cols].mean(axis=1)
        reliability_rows.append({
            "construct": construct,
            "cronbach_alpha": round(cronbach_alpha(scored[cols]), 3),
        })
    scored["promotion_response"] = scored["promotion_response"].fillna(
        scored["promotion_response"].median()
    )
    return scored, pd.DataFrame(reliability_rows)


def assign_business_segment_names(profiles: pd.DataFrame) -> dict[int, str]:
    remaining = set(profiles.index.tolist())
    mapping = {}
    for label, feature in [
        ("Value Seekers", "price_sensitivity"),
        ("Digital Trend Explorers", "digital_influence"),
        ("Convenience Loyalists", "convenience_orientation"),
    ]:
        candidate = profiles.loc[list(remaining), feature].idxmax()
        mapping[int(candidate)] = label
        remaining.remove(candidate)
    mapping[int(remaining.pop())] = "Quality & Wellness Enthusiasts"
    return mapping


def perform_segmentation(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    standardized = StandardScaler().fit_transform(data[SEGMENTATION_FEATURES])
    diagnostics = []
    for k in range(2, 7):
        labels = KMeans(n_clusters=k, random_state=RANDOM_SEED, n_init=30).fit_predict(standardized)
        diagnostics.append({"k": k, "silhouette_score": silhouette_score(standardized, labels)})
    model = KMeans(n_clusters=4, random_state=RANDOM_SEED, n_init=50)
    labels = model.fit_predict(standardized)
    profiles = pd.DataFrame(standardized, columns=SEGMENTATION_FEATURES).assign(cluster=labels).groupby("cluster").mean()
    mapping = assign_business_segment_names(profiles)
    segmented = data.copy()
    segmented["segment"] = pd.Series(labels, index=data.index).map(mapping)
    return segmented, pd.DataFrame(diagnostics)


def fit_purchase_intention_model(data: pd.DataFrame):
    threshold = data["new_product_intention"].quantile(0.65)
    outcome = (data["new_product_intention"] >= threshold).astype(int)
    numeric = [
        "age", "household_size", "monthly_fmcg_spend_idr",
        "purchase_frequency_per_month", *SEGMENTATION_FEATURES[:-1],
    ]
    categorical = [
        "gender", "region", "monthly_income_band",
        "primary_shopping_channel", "most_purchased_category",
    ]
    preprocessing = ColumnTransformer([
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]), numeric),
        ("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", drop="if_binary")),
        ]), categorical),
    ])
    model = Pipeline([
        ("preprocessing", preprocessing),
        ("classifier", LogisticRegression(max_iter=2000, C=0.70, random_state=RANDOM_SEED)),
    ])
    predictors = data[numeric + categorical]
    x_train, x_test, y_train, y_test = train_test_split(
        predictors, outcome, test_size=0.25, random_state=RANDOM_SEED, stratify=outcome
    )
    model.fit(x_train, y_train)
    probability = model.predict_proba(x_test)[:, 1]
    prediction = (probability >= 0.50).astype(int)
    auc = roc_auc_score(y_test, probability)
    names = model.named_steps["preprocessing"].get_feature_names_out()
    coefs = model.named_steps["classifier"].coef_[0]
    drivers = pd.DataFrame({"feature": names, "coefficient": coefs}).assign(
        absolute_coefficient=lambda d: d["coefficient"].abs()
    ).sort_values("absolute_coefficient", ascending=False)
    report = pd.DataFrame(classification_report(y_test, prediction, output_dict=True)).T
    confusion = pd.DataFrame(
        confusion_matrix(y_test, prediction),
        index=["Observed low intention", "Observed high intention"],
        columns=["Predicted low intention", "Predicted high intention"],
    )
    metrics = {
        "purchase_intention_threshold": round(float(threshold), 3),
        "test_roc_auc": round(float(auc), 3),
        "test_accuracy": round(float((prediction == y_test).mean()), 3),
        "test_sample_size": int(len(y_test)),
        "high_intention_share_pct": round(float(outcome.mean() * 100), 1),
    }
    roc_display = RocCurveDisplay.from_predictions(y_test, probability)
    plt.close(roc_display.figure_)
    return metrics, drivers, report, confusion, roc_display


def save_outputs(data, reliability, diagnostics, model_metrics, drivers, classification, confusion):
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA.parent.mkdir(parents=True, exist_ok=True)
    sizes = data["segment"].value_counts().reindex(SEGMENT_ORDER).rename_axis("segment").reset_index(name="n")
    sizes["share_pct"] = (sizes["n"] / len(data) * 100).round(1)
    profiles = data.groupby("segment")[[
        *SEGMENTATION_FEATURES, "new_product_intention",
        "monthly_fmcg_spend_idr", "purchase_frequency_per_month",
    ]].mean().reindex(SEGMENT_ORDER).round(2)
    channel = pd.crosstab(data["segment"], data["primary_shopping_channel"], normalize="index").mul(100).reindex(SEGMENT_ORDER).round(1)
    category = pd.crosstab(data["segment"], data["most_purchased_category"], normalize="index").mul(100).reindex(SEGMENT_ORDER).round(1)
    key_metrics = {
        "n_respondents": int(len(data)),
        "n_segments": 4,
        "silhouette_score_k4": round(float(diagnostics.loc[diagnostics["k"] == 4, "silhouette_score"].iloc[0]), 3),
        "minimum_cronbach_alpha": round(float(reliability["cronbach_alpha"].min()), 3),
        "maximum_cronbach_alpha": round(float(reliability["cronbach_alpha"].max()), 3),
        "median_monthly_spend_idr": int(data["monthly_fmcg_spend_idr"].median()),
        **model_metrics,
    }
    sizes.to_csv(TABLE_DIR / "segment_sizes.csv", index=False)
    profiles.to_csv(TABLE_DIR / "segment_profiles.csv")
    channel.to_csv(TABLE_DIR / "channel_by_segment_pct.csv")
    category.to_csv(TABLE_DIR / "category_by_segment_pct.csv")
    diagnostics.to_csv(TABLE_DIR / "silhouette_scores.csv", index=False)
    reliability.to_csv(TABLE_DIR / "reliability_summary.csv", index=False)
    drivers.to_csv(TABLE_DIR / "purchase_intention_drivers.csv", index=False)
    classification.to_csv(TABLE_DIR / "classification_report.csv")
    confusion.to_csv(TABLE_DIR / "confusion_matrix.csv")
    (TABLE_DIR / "key_metrics.json").write_text(json.dumps(key_metrics, indent=2), encoding="utf-8")
    data.to_csv(PROCESSED_DATA, index=False)
    return key_metrics, sizes, profiles, channel


def save_figures(data, diagnostics, drivers, roc_display, sizes, profiles, channel):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(sizes["segment"], sizes["n"]); ax.set_ylabel("Consumers"); ax.set_title("Consumer segment distribution"); ax.tick_params(axis="x", rotation=18); fig.tight_layout()
    fig.savefig(FIGURE_DIR / "01_segment_sizes.png", dpi=180); fig.savefig(FIGURE_DIR / "01_segment_sizes.svg"); plt.close(fig)
    cols = SEGMENTATION_FEATURES + ["new_product_intention"]
    z = (profiles[cols] - profiles[cols].mean()) / profiles[cols].std(ddof=0)
    fig, ax = plt.subplots(figsize=(11, 5.5)); image = ax.imshow(z, aspect="auto"); fig.colorbar(image, ax=ax, label="Standardized segment profile")
    ax.set_xticks(range(len(cols))); ax.set_xticklabels([c.replace("_", " ").title() for c in cols], rotation=35, ha="right"); ax.set_yticks(range(len(SEGMENT_ORDER))); ax.set_yticklabels(SEGMENT_ORDER); ax.set_title("Attitudinal and behavioral profile by segment"); fig.tight_layout()
    fig.savefig(FIGURE_DIR / "02_segment_profile_heatmap.png", dpi=180); fig.savefig(FIGURE_DIR / "02_segment_profile_heatmap.svg"); plt.close(fig)
    ax = channel.plot(kind="bar", stacked=True, figsize=(10, 5.5)); ax.set_ylabel("Share within segment (%)"); ax.set_title("Primary shopping channel by consumer segment"); ax.tick_params(axis="x", rotation=18); ax.legend(title="Channel", bbox_to_anchor=(1.02, 1), loc="upper left"); ax.figure.tight_layout()
    ax.figure.savefig(FIGURE_DIR / "03_channel_by_segment.png", dpi=180); ax.figure.savefig(FIGURE_DIR / "03_channel_by_segment.svg"); plt.close(ax.figure)
    spend = data.groupby("segment")["monthly_fmcg_spend_idr"].mean().reindex(SEGMENT_ORDER) / 1_000_000
    fig, ax = plt.subplots(figsize=(9, 5)); ax.bar(spend.index, spend.values); ax.set_ylabel("Average monthly spend (IDR million)"); ax.set_title("Average monthly FMCG spend by segment"); ax.tick_params(axis="x", rotation=18); fig.tight_layout()
    fig.savefig(FIGURE_DIR / "04_spend_by_segment.png", dpi=180); fig.savefig(FIGURE_DIR / "04_spend_by_segment.svg"); plt.close(fig)
    top = drivers.head(12).sort_values("coefficient"); labels = top["feature"].str.replace("numeric__", "", regex=False).str.replace("categorical__", "", regex=False).str.replace("_", " ", regex=False)
    fig, ax = plt.subplots(figsize=(9, 6)); ax.barh(labels, top["coefficient"]); ax.axvline(0, linewidth=1); ax.set_xlabel("Logistic-regression coefficient"); ax.set_title("Strongest adjusted signals of high new-product intention"); fig.tight_layout()
    fig.savefig(FIGURE_DIR / "05_purchase_intention_drivers.png", dpi=180); fig.savefig(FIGURE_DIR / "05_purchase_intention_drivers.svg"); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7.5, 4.5)); ax.plot(diagnostics["k"], diagnostics["silhouette_score"], marker="o"); ax.set_xlabel("Number of clusters"); ax.set_ylabel("Silhouette score"); ax.set_title("K-means cluster diagnostic"); ax.set_xticks(diagnostics["k"]); fig.tight_layout()
    fig.savefig(FIGURE_DIR / "06_silhouette_scores.png", dpi=180); fig.savefig(FIGURE_DIR / "06_silhouette_scores.svg"); plt.close(fig)
    fig, ax = plt.subplots(figsize=(6, 5)); ax.plot(roc_display.fpr, roc_display.tpr, label=f"ROC-AUC = {roc_display.roc_auc:.3f}"); ax.plot([0, 1], [0, 1], linestyle="--"); ax.set_xlabel("False-positive rate"); ax.set_ylabel("True-positive rate"); ax.set_title("Purchase-intention model: holdout ROC curve"); ax.legend(loc="lower right"); fig.tight_layout()
    fig.savefig(FIGURE_DIR / "07_purchase_intention_roc_curve.png", dpi=180); fig.savefig(FIGURE_DIR / "07_purchase_intention_roc_curve.svg"); plt.close(fig)


def main() -> None:
    if not RAW_DATA.exists():
        raise FileNotFoundError(f"Raw data not found at {RAW_DATA}. Run 01_Generate_Synthetic_Data.py first.")
    raw = pd.read_csv(RAW_DATA)
    scored, reliability = construct_scale_scores(raw)
    segmented, diagnostics = perform_segmentation(scored)
    model_metrics, drivers, classification, confusion, roc_display = fit_purchase_intention_model(segmented)
    key_metrics, sizes, profiles, channel = save_outputs(segmented, reliability, diagnostics, model_metrics, drivers, classification, confusion)
    save_figures(segmented, diagnostics, drivers, roc_display, sizes, profiles, channel)
    print(json.dumps(key_metrics, indent=2))


if __name__ == "__main__":
    main()

"""Generate a reproducible synthetic FMCG consumer survey dataset.

The data are designed for a portfolio case study. They imitate plausible
consumer heterogeneity but are not collected from real respondents and must
not be interpreted as market estimates.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

RANDOM_SEED = 20260721
N_RESPONDENTS = 800

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "03_Data" / "raw" / "fmcg_consumer_survey_synthetic.csv"

SEGMENTS = {
    "Value Seekers": {
        "weight": 0.30,
        "means": {
            "price": 4.45,
            "promo": 4.35,
            "quality": 3.35,
            "health": 3.05,
            "sustainability": 2.75,
            "digital": 3.20,
            "convenience": 3.55,
            "trust": 3.15,
            "innovation": 3.05,
        },
        "age_mean": 29,
        "income_probs": [0.34, 0.37, 0.21, 0.08],
        "channel_probs": [0.39, 0.20, 0.18, 0.23],
        "switch_probs": [0.05, 0.20, 0.47, 0.28],
        "spend_base": 680_000,
        "frequency_base": 7.6,
    },
    "Quality & Wellness Enthusiasts": {
        "weight": 0.24,
        "means": {
            "price": 2.65,
            "promo": 3.00,
            "quality": 4.55,
            "health": 4.50,
            "sustainability": 3.95,
            "digital": 3.45,
            "convenience": 3.65,
            "trust": 4.35,
            "innovation": 4.05,
        },
        "age_mean": 34,
        "income_probs": [0.08, 0.25, 0.40, 0.27],
        "channel_probs": [0.18, 0.36, 0.36, 0.10],
        "switch_probs": [0.20, 0.47, 0.27, 0.06],
        "spend_base": 1_260_000,
        "frequency_base": 9.1,
    },
    "Digital Trend Explorers": {
        "weight": 0.22,
        "means": {
            "price": 3.25,
            "promo": 3.75,
            "quality": 3.85,
            "health": 3.55,
            "sustainability": 3.45,
            "digital": 4.65,
            "convenience": 4.15,
            "trust": 3.20,
            "innovation": 4.65,
        },
        "age_mean": 25,
        "income_probs": [0.26, 0.40, 0.25, 0.09],
        "channel_probs": [0.18, 0.15, 0.59, 0.08],
        "switch_probs": [0.03, 0.12, 0.40, 0.45],
        "spend_base": 920_000,
        "frequency_base": 8.5,
    },
    "Convenience Loyalists": {
        "weight": 0.24,
        "means": {
            "price": 3.15,
            "promo": 2.85,
            "quality": 3.95,
            "health": 3.30,
            "sustainability": 2.95,
            "digital": 2.75,
            "convenience": 4.65,
            "trust": 4.50,
            "innovation": 3.25,
        },
        "age_mean": 38,
        "income_probs": [0.10, 0.31, 0.38, 0.21],
        "channel_probs": [0.49, 0.28, 0.16, 0.07],
        "switch_probs": [0.36, 0.48, 0.14, 0.02],
        "spend_base": 1_080_000,
        "frequency_base": 10.0,
    },
}

INCOME_BANDS = ["< IDR 5M", "IDR 5–10M", "IDR 10–20M", "> IDR 20M"]
CHANNELS = ["Minimarket", "Supermarket", "E-commerce", "Traditional market"]
SWITCH_LEVELS = ["Never", "Rarely", "Sometimes", "Often"]
REGIONS = ["Java", "Sumatra", "Kalimantan", "Sulawesi", "Bali & Nusa Tenggara"]
REGION_PROBS = [0.57, 0.19, 0.08, 0.10, 0.06]
GENDERS = ["Woman", "Man"]


def likert_items(rng: np.random.Generator, latent_mean: float, n: int, loading: float = 0.78) -> list[int]:
    """Create three correlated 1–5 Likert items from a latent construct."""
    latent = rng.normal(latent_mean, 0.55)
    items = []
    for _ in range(n):
        raw = loading * latent + (1 - loading) * 3 + rng.normal(0, 0.38)
        items.append(int(np.clip(np.rint(raw), 1, 5)))
    return items


def generate_dataset() -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_SEED)
    names = list(SEGMENTS)
    weights = [SEGMENTS[name]["weight"] for name in names]
    latent_segments = rng.choice(names, size=N_RESPONDENTS, p=weights)

    rows: list[dict] = []
    for i, segment_name in enumerate(latent_segments, start=1):
        config = SEGMENTS[segment_name]
        means = config["means"]

        age = int(np.clip(np.rint(rng.normal(config["age_mean"], 7.0)), 18, 55))
        gender = rng.choice(GENDERS, p=[0.57, 0.43])
        income_band = rng.choice(INCOME_BANDS, p=config["income_probs"])
        region = rng.choice(REGIONS, p=REGION_PROBS)
        channel = rng.choice(CHANNELS, p=config["channel_probs"])
        switching = rng.choice(SWITCH_LEVELS, p=config["switch_probs"])
        household_size = int(np.clip(rng.poisson(2.2) + 1, 1, 7))

        price_items = likert_items(rng, means["price"], 3)
        quality_items = likert_items(rng, means["quality"], 3)
        health_items = likert_items(rng, means["health"], 3)
        sustainability_items = likert_items(rng, means["sustainability"], 3)
        digital_items = likert_items(rng, means["digital"], 3)
        convenience_items = likert_items(rng, means["convenience"], 3)
        trust_items = likert_items(rng, means["trust"], 3)
        innovation_items = likert_items(rng, means["innovation"], 3)

        income_multiplier = {
            "< IDR 5M": 0.82,
            "IDR 5–10M": 0.97,
            "IDR 10–20M": 1.15,
            "> IDR 20M": 1.38,
        }[income_band]
        spend = config["spend_base"] * income_multiplier * rng.lognormal(0, 0.22)
        spend = int(np.clip(np.rint(spend / 10_000) * 10_000, 250_000, 3_500_000))
        frequency = int(np.clip(np.rint(rng.normal(config["frequency_base"], 2.0)), 2, 18))

        category = rng.choice(
            ["Personal care", "Home care", "Food & beverages"],
            p={
                "Value Seekers": [0.30, 0.31, 0.39],
                "Quality & Wellness Enthusiasts": [0.43, 0.22, 0.35],
                "Digital Trend Explorers": [0.51, 0.17, 0.32],
                "Convenience Loyalists": [0.28, 0.35, 0.37],
            }[segment_name],
        )

        rows.append(
            {
                "respondent_id": f"R{i:04d}",
                "age": age,
                "gender": gender,
                "region": region,
                "monthly_income_band": income_band,
                "household_size": household_size,
                "primary_shopping_channel": channel,
                "most_purchased_category": category,
                "monthly_fmcg_spend_idr": spend,
                "purchase_frequency_per_month": frequency,
                "brand_switching_frequency": switching,
                "promotion_response": int(np.clip(np.rint(rng.normal(means["promo"], 0.65)), 1, 5)),
                "price_sensitive_1": price_items[0],
                "price_sensitive_2": price_items[1],
                "price_sensitive_3": price_items[2],
                "quality_orientation_1": quality_items[0],
                "quality_orientation_2": quality_items[1],
                "quality_orientation_3": quality_items[2],
                "health_wellness_1": health_items[0],
                "health_wellness_2": health_items[1],
                "health_wellness_3": health_items[2],
                "sustainability_1": sustainability_items[0],
                "sustainability_2": sustainability_items[1],
                "sustainability_3": sustainability_items[2],
                "digital_influence_1": digital_items[0],
                "digital_influence_2": digital_items[1],
                "digital_influence_3": digital_items[2],
                "convenience_orientation_1": convenience_items[0],
                "convenience_orientation_2": convenience_items[1],
                "convenience_orientation_3": convenience_items[2],
                "brand_trust_1": trust_items[0],
                "brand_trust_2": trust_items[1],
                "brand_trust_3": trust_items[2],
                "new_product_intention_1": innovation_items[0],
                "new_product_intention_2": innovation_items[1],
                "new_product_intention_3": innovation_items[2],
            }
        )

    df = pd.DataFrame(rows)
    for col in ["monthly_income_band", "promotion_response", "sustainability_3"]:
        missing_idx = rng.choice(df.index, size=round(0.01 * len(df)), replace=False)
        df.loc[missing_idx, col] = np.nan
    return df


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = generate_dataset()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(df):,} rows at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

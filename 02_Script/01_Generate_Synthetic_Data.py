"""Generate a reproducible synthetic FMCG consumer survey dataset.

The dataset is designed only for portfolio demonstration. It must not be
interpreted as an estimate of the Indonesian FMCG market.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_SEED = 20260721
N_RESPONDENTS = 800
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "03_Data" / "raw" / "fmcg_consumer_survey_synthetic.csv"

SEGMENTS = [
    "Value Seekers",
    "Digital Trend Explorers",
    "Convenience Loyalists",
    "Quality & Wellness Enthusiasts",
]
SEGMENT_WEIGHTS = [0.30, 0.25, 0.23, 0.22]

CONSTRUCTS = [
    "price_sensitivity",
    "quality_orientation",
    "health_orientation",
    "sustainability_orientation",
    "digital_influence",
    "convenience_orientation",
    "brand_trust",
    "new_product_intention",
]

SEGMENT_MEANS = {
    "Value Seekers": [4.4, 3.3, 3.0, 2.8, 3.2, 3.5, 3.1, 3.0],
    "Digital Trend Explorers": [3.2, 3.8, 3.5, 3.4, 4.6, 4.1, 3.2, 4.6],
    "Convenience Loyalists": [3.1, 3.9, 3.3, 3.0, 2.8, 4.6, 4.5, 3.2],
    "Quality & Wellness Enthusiasts": [2.7, 4.6, 4.5, 4.0, 3.5, 3.7, 4.4, 4.1],
}

CHANNEL_PROBABILITIES = {
    "Value Seekers": [0.38, 0.20, 0.18, 0.24],
    "Digital Trend Explorers": [0.18, 0.15, 0.59, 0.08],
    "Convenience Loyalists": [0.50, 0.28, 0.16, 0.06],
    "Quality & Wellness Enthusiasts": [0.20, 0.35, 0.35, 0.10],
}

INCOME_PROBABILITIES = {
    "Value Seekers": [0.34, 0.37, 0.21, 0.08],
    "Digital Trend Explorers": [0.25, 0.40, 0.26, 0.09],
    "Convenience Loyalists": [0.10, 0.31, 0.38, 0.21],
    "Quality & Wellness Enthusiasts": [0.08, 0.25, 0.40, 0.27],
}

BASE_SPEND = {
    "Value Seekers": 680_000,
    "Digital Trend Explorers": 920_000,
    "Convenience Loyalists": 1_080_000,
    "Quality & Wellness Enthusiasts": 1_260_000,
}

BASE_FREQUENCY = {
    "Value Seekers": 8,
    "Digital Trend Explorers": 9,
    "Convenience Loyalists": 10,
    "Quality & Wellness Enthusiasts": 9,
}

AGE_MEANS = {
    "Value Seekers": 29,
    "Digital Trend Explorers": 25,
    "Convenience Loyalists": 38,
    "Quality & Wellness Enthusiasts": 34,
}


def _likert_item(rng: np.random.Generator, latent_score: float) -> int:
    observed = 0.85 * latent_score + 0.15 * 3 + rng.normal(0, 0.28)
    return int(np.clip(np.rint(observed), 1, 5))


def generate_dataset(n: int = N_RESPONDENTS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Return a synthetic FMCG consumer survey dataset."""
    rng = np.random.default_rng(seed)
    latent_segments = rng.choice(SEGMENTS, n, p=SEGMENT_WEIGHTS)
    rows: list[dict[str, object]] = []

    for respondent_number, segment in enumerate(latent_segments, start=1):
        age = int(np.clip(rng.normal(AGE_MEANS[segment], 7), 18, 55))
        income_band = rng.choice(
            ["< IDR 5M", "IDR 5-10M", "IDR 10-20M", "> IDR 20M"],
            p=INCOME_PROBABILITIES[segment],
        )
        promotion_mean = 4.3 if segment == "Value Seekers" else 3.3

        row: dict[str, object] = {
            "respondent_id": f"R{respondent_number:04d}",
            "age": age,
            "gender": rng.choice(["Woman", "Man"], p=[0.57, 0.43]),
            "region": rng.choice(
                ["Java", "Sumatra", "Kalimantan", "Sulawesi", "Bali & Nusa Tenggara"],
                p=[0.57, 0.19, 0.08, 0.10, 0.06],
            ),
            "monthly_income_band": income_band,
            "household_size": int(np.clip(rng.poisson(2.2) + 1, 1, 7)),
            "primary_shopping_channel": rng.choice(
                ["Minimarket", "Supermarket", "E-commerce", "Traditional market"],
                p=CHANNEL_PROBABILITIES[segment],
            ),
            "most_purchased_category": rng.choice(
                ["Personal care", "Home care", "Food & beverages"],
                p=[0.36, 0.29, 0.35],
            ),
            "monthly_fmcg_spend_idr": int(
                np.clip(
                    rng.lognormal(np.log(BASE_SPEND[segment]), 0.24) // 10_000 * 10_000,
                    250_000,
                    3_500_000,
                )
            ),
            "purchase_frequency_per_month": int(
                np.clip(np.rint(rng.normal(BASE_FREQUENCY[segment], 2)), 2, 18)
            ),
            "promotion_response": int(
                np.clip(np.rint(rng.normal(promotion_mean, 0.70)), 1, 5)
            ),
        }

        for construct, construct_mean in zip(CONSTRUCTS, SEGMENT_MEANS[segment]):
            latent_score = rng.normal(construct_mean, 0.50)
            for item_number in range(1, 4):
                row[f"{construct}_{item_number}"] = _likert_item(rng, latent_score)

        rows.append(row)

    data = pd.DataFrame(rows)

    for column in [
        "monthly_income_band",
        "promotion_response",
        "sustainability_orientation_3",
    ]:
        missing_index = rng.choice(data.index, 8, replace=False)
        data.loc[missing_index, column] = np.nan

    return data


def main() -> None:
    data = generate_dataset()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(data):,} synthetic respondents at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

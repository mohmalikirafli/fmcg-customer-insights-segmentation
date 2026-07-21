"""Normalize generated survey column names for the analysis pipeline."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "03_Data" / "raw" / "fmcg_consumer_survey_synthetic.csv"

ALIASES = {
    "price_sensitive_1": "price_sensitivity_1",
    "price_sensitive_2": "price_sensitivity_2",
    "price_sensitive_3": "price_sensitivity_3",
    "health_wellness_1": "health_orientation_1",
    "health_wellness_2": "health_orientation_2",
    "health_wellness_3": "health_orientation_3",
    "sustainability_1": "sustainability_orientation_1",
    "sustainability_2": "sustainability_orientation_2",
    "sustainability_3": "sustainability_orientation_3",
}


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    data = data.rename(columns=ALIASES)
    data.to_csv(DATA_PATH, index=False)
    print(f"Normalized columns at {DATA_PATH}")


if __name__ == "__main__":
    main()

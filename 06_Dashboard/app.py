"""Interactive dashboard for the synthetic FMCG customer-insights case study."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "03_Data" / "processed" / "fmcg_consumer_scored.csv"

st.set_page_config(page_title="FMCG Customer Insights", layout="wide")
st.title("FMCG Customer Insights Dashboard")
st.caption("Synthetic portfolio case study - not a real market estimate")

if not DATA_PATH.exists():
    st.warning(
        "Run `python 02_Script/01_Generate_Synthetic_Data.py` and "
        "`python 02_Script/02_FMCG_Customer_Insights_Analysis.py` first."
    )
    st.stop()

consumer_data = pd.read_csv(DATA_PATH)
segments = sorted(consumer_data["segment"].dropna().unique())
selected_segments = st.sidebar.multiselect(
    "Consumer segment", segments, default=segments
)
filtered = consumer_data[consumer_data["segment"].isin(selected_segments)]

metric_1, metric_2, metric_3 = st.columns(3)
metric_1.metric("Consumers", f"{len(filtered):,}")
metric_2.metric(
    "Median monthly spend",
    f"IDR {filtered['monthly_fmcg_spend_idr'].median() / 1_000_000:.2f}M",
)
metric_3.metric(
    "Average purchase frequency",
    f"{filtered['purchase_frequency_per_month'].mean():.1f} times/month",
)

left, right = st.columns(2)
with left:
    segment_share = (
        filtered["segment"].value_counts().rename_axis("segment").reset_index(name="consumers")
    )
    st.plotly_chart(
        px.bar(segment_share, x="segment", y="consumers", title="Segment size"),
        use_container_width=True,
    )

with right:
    channel_mix = (
        pd.crosstab(
            filtered["segment"],
            filtered["primary_shopping_channel"],
            normalize="index",
        )
        .mul(100)
        .reset_index()
        .melt("segment", var_name="channel", value_name="share_pct")
    )
    st.plotly_chart(
        px.bar(
            channel_mix,
            x="segment",
            y="share_pct",
            color="channel",
            title="Primary shopping channel",
            barmode="stack",
        ),
        use_container_width=True,
    )

traits = [
    "price_sensitivity",
    "quality_orientation",
    "health_orientation",
    "sustainability_orientation",
    "digital_influence",
    "convenience_orientation",
    "brand_trust",
    "new_product_intention",
]
profile = (
    filtered.groupby("segment")[traits]
    .mean()
    .reset_index()
    .melt("segment", var_name="trait", value_name="score")
)
st.plotly_chart(
    px.line(
        profile,
        x="trait",
        y="score",
        color="segment",
        markers=True,
        title="Consumer attitude profiles",
    ),
    use_container_width=True,
)

st.subheader("Synthetic consumer-level data")
st.dataframe(
    filtered[
        [
            "respondent_id",
            "segment",
            "age",
            "monthly_income_band",
            "primary_shopping_channel",
            "monthly_fmcg_spend_idr",
            "new_product_intention",
        ]
    ],
    use_container_width=True,
)

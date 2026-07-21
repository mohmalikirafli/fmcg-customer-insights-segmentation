# FMCG Customer Insights: Consumer Segmentation & Purchase Drivers

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Analysis](https://img.shields.io/badge/Focus-Customer%20Insights-success)](#business-context)
[![Data](https://img.shields.io/badge/Data-Synthetic-orange)](data/README.md)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

An end-to-end customer insight case study that translates FMCG consumer attitudes and shopping behaviour into **actionable segments, purchase drivers, and brand recommendations**.

> **Portfolio purpose:** demonstrate how my background in biostatistics, survey analysis, and data science can support Customer Market Insights decisions in an FMCG environment.

![Segment profile heatmap](outputs/figures/02_segment_profile_heatmap.png)

## Executive snapshot

| Metric | Result |
|---|---:|
| Consumer profiles analysed | **800** |
| Actionable segments | **4** |
| Scale reliability | **Cronbach's α 0.80–0.86** |
| Four-segment silhouette score | **0.202** |
| Purchase-intention model ROC-AUC | **0.813** |
| Consumers with high new-product intention | **35.0%** |
| Median monthly FMCG spend | **IDR 970,000** |

## Business context

FMCG teams need to understand not only **who buys**, but also **why consumers choose, switch, trust, and try products**. This project addresses three decision questions:

1. Which consumer groups are meaningfully different in their motivations and behaviour?
2. Which factors are associated with willingness to try a new FMCG product?
3. How should product, message, promotion, and channel strategy differ by segment?

The workflow is aligned with typical Customer Market Insights responsibilities: uncovering motivations and behaviours, translating research into clear insight, and supporting brand strategy, innovation, and in-market execution.

## Key findings

### 1. Four consumer segments

| Segment | Share | Core characteristics | Commercial implication |
|---|---:|---|---|
| **Value Seekers** | 29.9% | Highest price sensitivity and promotion response; lowest spend | Use pack-price architecture, targeted bundles, and visible value cues |
| **Digital Trend Explorers** | 25.4% | Highest digital influence and new-product intention; e-commerce led | Prioritise creator seeding, social commerce, reviews, and launch trials |
| **Convenience Loyalists** | 23.4% | Highest brand trust, convenience orientation, and purchase frequency | Protect availability, simplify repurchase, and reinforce trusted claims |
| **Quality & Wellness Enthusiasts** | 21.4% | Highest quality, health orientation, and monthly spend | Lead with superior benefits, credible evidence, and premium innovation |

![Segment sizes](outputs/figures/01_segment_sizes.png)

### 2. Channels are segment-specific

- **58.1%** of Digital Trend Explorers primarily shop through e-commerce.
- **50.3%** of Convenience Loyalists primarily use minimarkets.
- Quality & Wellness Enthusiasts are split between supermarkets and e-commerce.
- Value Seekers have the highest traditional-market share and a strong minimarket presence.

![Channel mix](outputs/figures/03_channel_by_segment.png)

### 3. High-intention consumers are identifiable

The interpretable logistic-regression model achieved **ROC-AUC 0.813**. Strong positive signals included digital influence, higher income bands, quality orientation, and sustainability orientation. Age showed a negative association after adjustment, indicating greater new-product openness among younger consumers in this synthetic case study.

![Purchase intention drivers](outputs/figures/05_purchase_intention_drivers.png)

## Recommended actions

| Decision area | Recommendation |
|---|---|
| **Innovation launch** | Use Digital Trend Explorers as the first trial and advocacy audience; emphasise digital discovery, reviews, and e-commerce availability |
| **Premium growth** | Target Quality & Wellness Enthusiasts with evidence-led functional benefits and stronger ingredient or wellness narratives |
| **Retention** | Protect Convenience Loyalists through dependable availability, trusted performance, and frictionless repeat purchase |
| **Value strategy** | Offer Value Seekers clear value through bundles, price ladders, and targeted promotions without weakening the core proposition |
| **Measurement** | Track trial-to-repeat conversion, segment-level uplift, channel conversion, and movement between segments |

## Methods

- Survey-scale construction and Cronbach's alpha
- Descriptive and behavioural profiling
- K-means clustering with silhouette diagnostics
- Logistic regression for purchase intention
- Holdout evaluation using ROC-AUC
- Reproducible data generation, notebook, dashboard, and CI

## Reproduce the analysis

```bash
git clone https://github.com/mohmalikirafli/fmcg-customer-insights-segmentation.git
cd fmcg-customer-insights-segmentation
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py
python src/analyze.py
streamlit run app.py
```

## Data integrity and limitations

The dataset is **synthetic and reproducibly generated**. It demonstrates an analytical workflow and must not be interpreted as a real Indonesian market estimate. Commercial recommendations should be validated using observed survey, panel, retail-audit, social-listening, or transaction data.

## Author

**Mohammad Maliki Rafli**  
Master of Public Health Candidate — Biostatistics & Health Data Science  
GitHub: [@mohmalikirafli](https://github.com/mohmalikirafli)

---

*Independent portfolio project. Not affiliated with or endorsed by any FMCG company.*
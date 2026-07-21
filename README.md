# FMCG Customer Insights: Consumer Segmentation and Purchase Drivers

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E?logo=scikitlearn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Domain](https://img.shields.io/badge/Domain-Customer%20Insights-0067B1)
![Data](https://img.shields.io/badge/Data-Synthetic-6F42C1)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end customer-insights portfolio project that translates synthetic FMCG consumer survey data into **actionable consumer segments, purchase-intention drivers, channel insights, and business recommendations**.

**Author:** Mohammad Maliki Rafli  
**Program:** Master of Public Health - Biostatistics and Health Data Science, Universitas Airlangga

## Table of Contents

- [Project Overview](#project-overview)
- [Final Presentation](#final-presentation)
- [Business Objective](#business-objective)
- [Repository Structure](#repository-structure)
- [Analytical Workflow](#analytical-workflow)
- [Methods](#methods)
- [Key Results](#key-results)
- [Selected Visualizations](#selected-visualizations)
- [Business Recommendations](#business-recommendations)
- [Data Integrity and Limitations](#data-integrity-and-limitations)
- [Reproducing the Analysis](#reproducing-the-analysis)
- [Interactive Dashboard](#interactive-dashboard)
- [License and Portfolio Use](#license-and-portfolio-use)
- [Contact](#contact)

## Project Overview

FMCG teams need to understand not only **who buys**, but also **why consumers choose, trust, switch, and try products**. This portfolio case study demonstrates how consumer-research data can be transformed into decision-ready evidence for brand strategy, innovation, communication, channel planning, and market execution.

The project addresses three business questions:

1. Which consumer groups differ meaningfully in their motivations and shopping behaviour?
2. Which factors are associated with willingness to try a new FMCG product?
3. How should product, message, promotion, and channel strategies differ by segment?

## Final Presentation

The final portfolio presentation contains **11 professionally designed slides** and supersedes the earlier automatically generated executive-summary presentation.

- [View the final portfolio presentation (PDF)](05_Presentation/FMCG_Customer_Insights_Portfolio_Presentation.pdf)
- [Open the executed analysis notebook](02_Script/FMCG_Customer_Insights_Analysis.ipynb)

## Business Objective

To identify actionable FMCG consumer segments, profile their motivations and channel behaviour, and build an interpretable model of high new-product intention that can inform targeting, innovation launches, premium growth, value architecture, and retention strategy.

## Repository Structure

```text
.
├── 01_Report/
│   └── FMCG_Customer_Insights_Report.md
├── 02_Script/
│   ├── 01_Generate_Synthetic_Data.py
│   ├── 01b_Normalize_Columns.py
│   ├── 02_FMCG_Customer_Insights_Analysis.py
│   ├── 03_Build_Analysis_Notebook.py
│   └── FMCG_Customer_Insights_Analysis.ipynb
├── 03_Data/
│   ├── README.md
│   ├── data_dictionary.csv
│   ├── raw/
│   └── processed/
├── 04_Output/
│   ├── figures/
│   │   └── *.png
│   └── tables/
│       └── *.csv / *.json
├── 05_Presentation/
│   ├── FMCG_Customer_Insights_Portfolio_Presentation.pdf
│   └── README.md
├── 06_Dashboard/
│   └── app.py
├── .github/workflows/
│   └── reproduce-analysis.yml
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Analytical Workflow

1. Generate a reproducible synthetic survey of 800 FMCG consumers.
2. Introduce limited missingness to demonstrate explicit preprocessing.
3. Construct eight multi-item consumer scales and assess internal consistency.
4. Standardize the segmentation variables and compare K-means solutions.
5. Select a four-cluster solution and translate clusters into business personas.
6. Profile segment size, attitudes, spending, frequency, and shopping channel.
7. Model high new-product intention using interpretable logistic regression.
8. Translate statistical findings into segment-specific commercial actions.

## Methods

### Consumer measurement

- Eight constructs measured using three Likert-scale items each
- Median imputation for limited item-level missingness
- Mean-scale scoring
- Cronbach's alpha for internal consistency

### Consumer segmentation

- Standardisation of attitudinal, behavioural, and promotional-response variables
- K-means clustering with repeated initialisation
- Silhouette diagnostics for two to six clusters
- Business naming based on dominant standardised characteristics

### Purchase-intention analysis

- Interpretable logistic regression
- Standardisation of numeric variables
- One-hot encoding of categorical variables
- Holdout evaluation using ROC-AUC
- Coefficient and odds-ratio interpretation

## Key Results

### Portfolio-level metrics

| Metric | Result |
|---|---:|
| Synthetic consumer profiles | **800** |
| Actionable consumer segments | **4** |
| Cronbach's alpha range | **0.798-0.861** |
| Four-cluster silhouette score | **0.202** |
| Purchase-intention model ROC-AUC | **0.813** |
| High new-product intention | **35.0%** |
| Median monthly FMCG spend | **IDR 970,000** |

### Consumer segments

| Segment | Share | Core motivation | Primary opportunity |
|---|---:|---|---|
| **Value Seekers** | **29.9%** | Price and promotions | Pack-price architecture, targeted bundles, and visible value cues |
| **Digital Trend Explorers** | **25.4%** | Digital discovery and novelty | Creator seeding, reviews, social commerce, and product trial |
| **Convenience Loyalists** | **23.4%** | Ease, trust, and repeat purchase | Availability, frictionless repurchase, and trusted performance |
| **Quality & Wellness Enthusiasts** | **21.4%** | Health, quality, and evidence | Premium innovation and credible benefit communication |

### Channel and spending evidence

- **58.1%** of Digital Trend Explorers primarily shop through e-commerce.
- **50.3%** of Convenience Loyalists primarily use minimarkets.
- Quality & Wellness Enthusiasts have the highest average monthly spending.
- Value Seekers show the strongest traditional-market presence.

## Selected Visualizations

The figures below are generated reproducibly by the analysis workflow. PNG is used to ensure reliable rendering in GitHub README pages.

### Consumer segment distribution

![Consumer segment distribution](04_Output/figures/01_segment_sizes.png)

### Segment profile heatmap

![Standardized segment profile heatmap](04_Output/figures/02_segment_profile_heatmap.png)

### Primary shopping channel by segment

![Primary shopping channel by segment](04_Output/figures/03_channel_by_segment.png)

### Purchase-intention drivers

![Purchase-intention model coefficients](04_Output/figures/05_purchase_intention_drivers.png)

## Business Recommendations

| Strategic pillar | Target segment | Recommended action |
|---|---|---|
| **Innovation launch** | Digital Trend Explorers | Use creator content, social commerce, launch trials, reviews, and rapid learning loops |
| **Premium growth** | Quality & Wellness Enthusiasts | Lead with credible functional benefits, ingredient evidence, and wellness positioning |
| **Retention** | Convenience Loyalists | Protect availability, simplify repeat purchase, and reinforce trusted performance |
| **Value architecture** | Value Seekers | Use bundles, pack-price ladders, and targeted promotions without weakening the core proposition |
| **Measurement** | All segments | Track segment-level conversion, repeat purchase, migration, and incremental sales |

## Data Integrity and Limitations

The dataset is **fully synthetic and reproducibly generated**. It contains no real respondents, confidential company information, or proprietary market data. The project demonstrates analytical reasoning, reproducibility, interpretation, and data storytelling; it does not provide a factual estimate of the Indonesian FMCG market.

Key limitations:

- Synthetic data cannot estimate actual prevalence, market size, or causal effects.
- Cluster labels summarise patterns and require validation using observed consumer data.
- The silhouette score indicates moderate rather than strong geometric separation.
- Logistic-regression coefficients describe adjusted associations, not causal effects.
- Commercial recommendations are hypotheses for testing, not direct market instructions.

## Reproducing the Analysis

```bash
git clone https://github.com/mohmalikirafli/fmcg-customer-insights-segmentation.git
cd fmcg-customer-insights-segmentation
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python 02_Script/01_Generate_Synthetic_Data.py
python 02_Script/01b_Normalize_Columns.py
python 02_Script/02_FMCG_Customer_Insights_Analysis.py
python 02_Script/03_Build_Analysis_Notebook.py
```

The GitHub Actions workflow automatically regenerates the data, notebook, tables, and PNG figures whenever the analytical scripts are updated.

## Interactive Dashboard

Run the Streamlit dashboard locally after generating the processed dataset:

```bash
streamlit run 06_Dashboard/app.py
```

## License and Portfolio Use

The source code is available under the [MIT License](LICENSE). The report, figures, presentation, and written interpretation remain the intellectual work of the author and should be attributed when adapted or referenced.

This independent portfolio project is intended for education, recruitment, and methodological discussion. It is not affiliated with or endorsed by Unilever or any other FMCG company.

## Contact

For questions, collaboration, or discussion, contact **Mohammad Maliki Rafli** through the [GitHub profile](https://github.com/mohmalikirafli) or open an [issue](https://github.com/mohmalikirafli/fmcg-customer-insights-segmentation/issues).

---

This repository demonstrates the transfer of biostatistics, survey analysis, and health data science skills into Customer Market Insights.

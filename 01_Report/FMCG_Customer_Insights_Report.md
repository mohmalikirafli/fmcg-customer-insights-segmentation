# FMCG Customer Insights Report

## Consumer Segmentation and Purchase Drivers

**Author:** Mohammad Maliki Rafli  
**Program:** Master of Public Health - Biostatistics and Health Data Science, Universitas Airlangga

> **Portfolio disclosure:** This report uses a fully synthetic and reproducibly generated dataset. Findings demonstrate an analytical workflow and are not estimates of the Indonesian FMCG market.

## Executive Summary

This project demonstrates an end-to-end Customer Market Insights workflow using 800 synthetic FMCG consumer profiles. The analysis evaluates multi-item survey scales, identifies four interpretable consumer segments through K-means clustering, examines channel and spending behavior, and models high new-product intention using logistic regression.

The four-segment solution produced a silhouette score of **0.242**, indicating moderate geometric separation. Scale reliability was good, with Cronbach's alpha ranging from **0.845 to 0.910**. The purchase-intention model achieved **ROC-AUC 0.849** and **accuracy 0.795** on a stratified holdout sample.

## Business Questions

1. Which consumer groups differ meaningfully in motivations and shopping behavior?
2. Which factors are associated with willingness to try a new FMCG product?
3. How should product, message, promotion, and channel strategies differ across segments?

## Data and Measurement

The synthetic dataset contains demographics, household characteristics, monthly FMCG spending, purchase frequency, shopping channel, most-purchased category, promotion response, and eight consumer-attitude constructs. Each construct is represented by three Likert-scale items.

The constructs are:

- Price sensitivity
- Quality orientation
- Health orientation
- Sustainability orientation
- Digital influence
- Convenience orientation
- Brand trust
- New-product intention

A small amount of missingness is intentionally introduced to demonstrate transparent preprocessing.

## Methods

### Scale construction

Item-level missing values are imputed using the median. Construct scores are calculated as the mean of three items. Internal consistency is assessed using Cronbach's alpha.

### Consumer segmentation

Seven attitudinal constructs and promotion response are standardized and entered into K-means clustering. Solutions from two to six clusters are compared using silhouette scores. The four-cluster solution is selected for business interpretability and adequate balance across segment sizes.

### Purchase-intention model

High new-product intention is defined using the 65th percentile of the intention score. Logistic regression is fitted using standardized numeric predictors and one-hot encoded categorical predictors. Performance is assessed on a stratified 25% holdout sample.

## Key Results

| Metric | Result |
|---|---:|
| Synthetic consumer profiles | 800 |
| Actionable segments | 4 |
| Cronbach's alpha range | 0.845-0.910 |
| Four-cluster silhouette score | 0.242 |
| Holdout ROC-AUC | 0.849 |
| Holdout accuracy | 0.795 |
| High new-product intention | 39.2% |
| Median monthly FMCG spend | IDR 930,000 |

## Segment Profiles

### Value Seekers — 29.9%

This segment has the highest price sensitivity and promotion response and the lowest average spending level. Recommended actions include pack-price architecture, bundles, targeted promotions, and clear value communication.

### Convenience Loyalists — 24.8%

This segment has the strongest convenience orientation and brand trust. Minimarkets are the dominant channel. Recommended actions include dependable availability, trusted performance, and frictionless repeat purchase.

### Digital Trend Explorers — 22.9%

This segment has the highest digital influence and new-product intention. E-commerce is the dominant shopping channel. Recommended actions include creator seeding, consumer reviews, social commerce, and launch trials.

### Quality & Wellness Enthusiasts — 22.5%

This segment has the strongest quality, health, and sustainability orientation and the highest average spending. Recommended actions include evidence-led benefits, ingredient transparency, and premium innovation.

## Channel Evidence

- 55.7% of Digital Trend Explorers primarily shop through e-commerce.
- 49.0% of Convenience Loyalists primarily use minimarkets.
- Quality & Wellness Enthusiasts use both e-commerce and supermarkets.
- Value Seekers have the strongest traditional-market presence.

## Purchase-Intention Evidence

The logistic-regression model achieved ROC-AUC 0.849. Stronger positive adjusted signals include digital influence, health orientation, e-commerce shopping, and purchase frequency. Price sensitivity and older age show negative adjusted associations.

These coefficients represent associations within a synthetic dataset. They are not causal effects.

## Recommendations

| Segment | Strategic objective | Recommended activation | Suggested KPI |
|---|---|---|---|
| Digital Trend Explorers | Launch trial and advocacy | Creator seeding, reviews, social commerce | Trial, conversion, repeat |
| Quality & Wellness Enthusiasts | Premium and functional growth | Evidence-led benefits and ingredient transparency | Premium conversion, trust |
| Convenience Loyalists | Retention and habitual repurchase | Availability and easy repurchase | Availability, retention, repeat |
| Value Seekers | Value architecture | Bundles and targeted promotions | Promotional uplift, margin |

## Limitations

- All records are synthetic.
- The segment structure is partly embedded in the data-generating process.
- The silhouette score indicates moderate rather than strong separation.
- Predictive performance is based on one internal holdout split.
- Regression coefficients are associative and not causal.
- Recommendations require validation with observed survey, transaction, panel, retail-audit, social-listening, experimental, or qualitative data.

## Conclusion

The project demonstrates how survey measurement, segmentation, predictive modeling, visualization, and business interpretation can be integrated into a transparent Customer Market Insights workflow. It is designed to show how biostatistics and data-science skills can transfer into FMCG consumer research and decision support.

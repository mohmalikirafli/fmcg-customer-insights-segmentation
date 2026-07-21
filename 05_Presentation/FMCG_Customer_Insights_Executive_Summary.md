# FMCG Customer Insights - Executive Summary

## 1. Business challenge

FMCG teams need to understand who their consumers are, what motivates purchase, where they shop, and who is most open to innovation. This portfolio case study converts consumer-research data into segmentation, purchase-intention drivers, and activation recommendations.

## 2. Analytical approach

- Reproducibly generated survey of 800 synthetic FMCG consumers
- Eight reliable multi-item consumer-attitude scales
- K-means clustering with silhouette diagnostics
- Segment profiling across spending, purchase frequency, channel, and attitudes
- Interpretable logistic regression for high new-product intention
- Holdout evaluation using ROC-AUC and classification metrics

## 3. Four actionable segments

| Segment | Share | Priority action |
|---|---:|---|
| Value Seekers | 29.9% | Bundles, price ladders, and visible value cues |
| Convenience Loyalists | 24.8% | Availability, trust, and frictionless repurchase |
| Digital Trend Explorers | 22.9% | Social discovery, reviews, and e-commerce trial |
| Quality & Wellness Enthusiasts | 22.5% | Evidence-led benefits and premium innovation |

## 4. Channel evidence

- 55.7% of Digital Trend Explorers primarily shop through e-commerce.
- 49.0% of Convenience Loyalists primarily use minimarkets.
- Quality & Wellness Enthusiasts use both e-commerce and supermarkets.
- Value Seekers have the strongest traditional-market presence.

## 5. Purchase-intention model

The holdout logistic-regression model achieved **ROC-AUC 0.849** and **accuracy 0.795**. Stronger positive adjusted signals included digital influence, health orientation, e-commerce shopping, and purchase frequency. Price sensitivity and age showed negative adjusted associations.

These coefficients represent associations within synthetic data and must not be interpreted as causal effects or real market findings.

## 6. Recommended activation

| Segment | Strategic objective | Activation | Suggested KPI |
|---|---|---|---|
| Digital Trend Explorers | Launch trial and advocacy | Creator seeding, reviews, social commerce | Trial, conversion, repeat |
| Quality & Wellness Enthusiasts | Premium and functional growth | Evidence-led benefits, ingredient transparency | Premium conversion, trust |
| Convenience Loyalists | Retention and habitual repurchase | Availability and easy repurchase | Availability, retention, repeat |
| Value Seekers | Value architecture | Bundles and targeted promotions | Promotional uplift, margin |

## Portfolio disclosure

This presentation is based on fully synthetic data and is intended to demonstrate Customer Market Insights reasoning, analytical methodology, reproducibility, and data storytelling.

# Customer Engagement & Retention Analytics

A reproducible Streamlit analytics project for studying customer engagement, product utilization, relationship depth, and churn risk in a European banking dataset.

## Project structure

```text
customer-engagement-retention-analytics/
├── app/streamlit_app.py
├── data/European_Bank.csv
├── notebooks/customer_retention_analysis.ipynb
├── src/data_cleaning.py
├── src/analysis.py
├── src/visualization.py
├── outputs/charts/
├── outputs/reports/
├── .gitignore
├── README.md
├── requirements.txt
└── LICENSE
```

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Open the local URL displayed by Streamlit. The dashboard supports geography, activity, product-count, balance, salary, and high-balance disengagement filters. It also provides a downloadable filtered customer risk list.

## Re-run the analysis

```bash
python src/analysis.py
```

The analysis module writes enriched customer data and KPI summaries to `outputs/`. Charts can be regenerated through `src/visualization.py` after loading the enriched dataset.

## Core definitions

High-balance customers are defined as customers at or above the sample 75th percentile of balance. Premium-risk customers are high-balance customers who are inactive. The Relationship Strength Index is a transparent descriptive score based on activity, product depth, and credit-card ownership. It is intended for prioritization and hypothesis generation, not automated credit or eligibility decisions.

## Analytical caution

The dataset is a cross-sectional snapshot. Reported relationships are descriptive and should not be interpreted as causal effects. Production use should add time-based engagement, campaign treatment, product-level detail, fairness monitoring, and controlled experiments.

# Customer Engagement and Product Utilization as Retention Signals

**Author:** Manus AI  
**Dataset:** European Bank customer records, 2025  
**Analytical scope:** Engagement, product depth, financial commitment, and descriptive retention strength

## Abstract

This study evaluates customer churn through behavior and relationship depth rather than demographics alone. The analysis uses 10,000 European bank customer records and examines activity status, number of products, credit-card ownership, account balance, and estimated salary. The overall churn rate is 20.37%. Inactive customers churn at 26.85%, compared with 14.27% for active customers. Customers with one product churn at 27.71%, compared with 12.77% among customers with two or more products. A high-value disengagement screen identifies 1,247 customers with balances at or above the sample 75th percentile and inactive status; this group has a 30.47% churn rate. The central implication is that balance alone is not a sufficient loyalty signal. Retention strategy should prioritize re-engagement and relationship deepening, especially for high-balance customers who use only one product.

## 1. Business question and analytical framing

Banks can misclassify customers as loyal when they rely on balance, salary, or tenure without observing recent engagement and relationship depth. This project therefore treats retention as a behavioral outcome. Engagement is represented by `IsActiveMember`, while relationship depth is represented primarily by `NumOfProducts` and secondarily by credit-card ownership. Balance is used to locate high-value customers, not as a direct proxy for loyalty.

The analysis is descriptive. It identifies segments with materially different observed churn rates, but it does not establish that activity or product adoption causes retention. Product and engagement interventions should be tested through controlled campaigns before being scaled.

## 2. Data validation and preparation

The source file contains 10,000 unique customers and 14 source columns. It has no missing cells, no duplicate customer IDs, and valid binary values for credit-card ownership, activity status, and churn. The analysis adds labels for activity, product tier, churn outcome, and engagement profile. It also computes a descriptive Relationship Strength Index that awards 50 points for activity, up to 35 points for product depth, and 15 points for credit-card ownership.

High balance is defined as a balance at or above the sample 75th percentile, **$127,644.24**. This threshold is deliberately transparent and can be adjusted in the dashboard. The high-value disengagement detector combines this balance threshold with inactive status.

## 3. Findings

### 3.1 Engagement is strongly associated with retention

Active customers churn at **14.27%**, while inactive customers churn at **26.85%**. The inactive group therefore has an observed churn rate **12.58 percentage points higher**, or **1.88 times** the active rate. This is the clearest engagement signal in the dataset. It supports a retention operating model that monitors inactivity before a customer becomes a confirmed churn event.

![Engagement and product churn](outputs/engagement_product_churn.png)

### 3.2 Two products are associated with substantially lower churn than one product

Customers with one product churn at **27.71%**. Customers with two or more products churn at **12.77%**, a difference of **14.94 percentage points**. The two-product segment has a 7.58% churn rate, but the three- and four-product segments show unusually high churn rates of 82.71% and 100%, respectively. These small segments should not be interpreted as evidence that more products always increase churn. They may reflect unusual, unstable, or incorrectly represented product combinations. The practical recommendation is to focus on relevant second-product adoption and investigate the product mix behind three- and four-product records.

### 3.3 High balance does not guarantee loyalty

The high-balance disengagement screen contains **1,247 customers**, or **12.47%** of the sample. Their churn rate is **30.47%**, materially above the 20.37% overall rate. This group illustrates the project’s main risk: premium customers can be financially valuable while behaviorally disengaged.

Average balances are similar for active and inactive customers in aggregate: approximately **$75,875** for active customers and **$77,134** for inactive customers. This small difference shows why balance by itself is a weak engagement substitute. The risk signal comes from the combination of high balance and inactivity.

![Balance, activity, and outcome](outputs/balance_activity_outcome.png)

### 3.4 The strongest practical segment is active, multi-product, and card-holding

A “sticky customer” is defined here as active, using at least two products, and holding a credit card. This group represents **18.32%** of customers and has a churn rate of **9.12%**. The result supports loyalty and bundling strategies that deepen relevant relationships while preserving active usage. Credit-card ownership alone has little separation in this sample: cardholders churn at 20.18% versus 20.81% for non-cardholders. The card should therefore be treated as a supporting relationship feature, not a standalone retention solution.

![Churn across engagement profiles](outputs/profile_churn.png)

### 3.5 Inactive, low-product customers are the broadest high-risk profile

The inactive, low-product profile contains **1,693 customers** and has a churn rate of **38.22%**. The inactive, high-balance profile has a lower but still elevated rate of **30.47%**. Active low-product customers churn at **18.92%**, which suggests that activity can partially offset shallow product depth. The most actionable prioritization is therefore not “sell more products to everyone.” It is to re-engage inactive customers first, then offer a relevant second product where the customer need is clear.

## 4. KPI definitions and results

| KPI | Definition | Result |
|---|---|---:|
| Engagement Retention Ratio | Inactive churn rate divided by active churn rate | 1.88x |
| Product Depth Index | Descriptive product count used in relationship score | 1–4 products |
| High-Balance Disengagement Rate | Inactive, high-balance customers divided by all customers | 12.47% |
| Credit Card Stickiness Score | Churn comparison for cardholders vs non-cardholders | 20.18% vs 20.81% |
| Relationship Strength Index | Activity, product depth, and card ownership composite | 0–100 |

## 5. Recommendations

**Create an inactivity early-warning workflow.** Use a recent-activity trigger to route inactive customers into a service or engagement journey. The first contact should diagnose reduced usage rather than immediately lead with a generic offer. The 12.58-point activity gap provides a meaningful business case for monitoring this signal.

**Prioritize high-balance disengaged customers.** The 1,247-customer risk pool should receive a differentiated treatment with relationship-manager outreach, digital usage prompts, and a review of whether the bank’s primary product still fits the customer. Retention value is likely higher for this group than for a broad, untargeted campaign.

**Use second-product adoption as a relationship-deepening objective.** One-product customers have materially higher churn than two-product customers. Recommended bundles should be need-based and measured by subsequent activity, not only by product opening. Avoid treating three- and four-product records as a success benchmark until their product mix and data quality are understood.

**Measure campaign outcomes by engagement and churn together.** The dashboard should be paired with a test-and-control framework. Key measures should include reactivation rate, second-product activation, 90-day retention, and customer complaints or opt-outs. A product sale without sustained usage should not be counted as a retention success.

## 6. Limitations and next analytical steps

The dataset is a cross-sectional snapshot, so it does not contain event dates, tenure histories over time, product identities, transaction frequency, contact history, or campaign exposure. `IsActiveMember` is a binary indicator and may conceal important differences in recency and intensity of use. The balance threshold is sample-relative, and the Relationship Strength Index is a prioritization heuristic rather than a validated predictive model.

The next phase should add monthly activity and transaction measures, product-level identifiers, service interactions, and campaign treatment flags. A validated churn model can then estimate incremental risk while fairness monitoring tests whether targeting creates unequal treatment across geography, gender, or age groups.

## 7. Reproducibility

Run `python3 analyze.py` from the project directory to regenerate the enriched dataset, metrics JSON, and charts. Run `streamlit run app.py` to open the live dashboard. The dashboard supports geography, activity, product-count, balance, salary, and high-value disengagement filters.

## References

[1]: `European_Bank (1).csv` "Project-provided European Bank customer dataset"

[2]: `outputs/metrics.json` "Reproducible analysis metrics and segment summaries"

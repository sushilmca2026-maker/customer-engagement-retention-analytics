# Executive Summary: Engagement-Driven Retention Strategy

## Decision message

The evidence supports a shift from balance-led retention to engagement-led retention. In this 10,000-customer banking dataset, inactive customers churn at **26.85%**, compared with **14.27%** for active customers. Customers with one product churn at **27.71%**, compared with **12.77%** for customers with two or more products. High-balance customers are not automatically loyal: the high-balance, inactive segment contains **1,247 customers** and churns at **30.47%**.

## Why this matters for public stakeholders

A bank that monitors only financial value can miss silent disengagement among customers who appear economically important. This creates avoidable household disruption, weakens trust, and can lead to generic interventions that do not address the underlying relationship problem. Engagement signals provide an earlier and more actionable view of retention risk.

The findings do not justify automated exclusion, differential pricing, or adverse decisions. They support proportionate, customer-centered outreach and service improvement. Any operational deployment should include human review, clear explanations, opt-out options, data minimization, and fairness monitoring.

## Priority actions

**First, establish an inactivity early-warning process.** Customers who become inactive should be offered a service check-in and relevant digital support before a churn event. The process should prioritize consent and problem resolution over indiscriminate sales activity.

**Second, protect high-value disengaged customers.** Customers with balances at or above **$127,644** and inactive status should receive a tailored review. This group represents **12.47%** of customers and has a churn rate well above the overall rate. The review should assess whether the customer’s primary needs are being met and whether access, usability, or service friction is limiting engagement.

**Third, encourage meaningful relationship depth.** Two-product customers show substantially lower churn than one-product customers. Product bundles should be based on customer needs and measured by ongoing use, not merely account opening. The unusually high churn among three- and four-product records should be investigated before using these records as a model for cross-sell success.

**Fourth, evaluate interventions transparently.** Use test-and-control designs with outcome measures covering reactivation, sustained product use, 90-day retention, complaints, and opt-outs. Publish aggregate results so that program effectiveness and unintended effects can be reviewed.

## Guardrails

The analysis is descriptive and based on a single snapshot. It cannot prove that activity or product count causes retention. The dashboard should therefore support prioritization and learning rather than automatic decisions. Age, gender, and geography should be monitored for disparate impact, while protected attributes should not be used as a shortcut for individual treatment.

## Delivery package

The accompanying dashboard provides live filtering by geography, activity, product count, balance, salary, and high-value disengagement. The research paper documents the methods, exact findings, limitations, and recommended operating model. The analysis pipeline regenerates all metrics and visualizations from the project-provided source file.

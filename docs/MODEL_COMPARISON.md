# Model Comparison & Evaluation Report

## Overview
We evaluated three baseline models (`Logistic Regression`, `Random Forest`, and `XGBoost`) on our test dataset split (80/20).

## Performance Summary
- **Tree-Based Models (Random Forest & XGBoost):** Achieved near-perfect classification metrics across accuracy, precision, and recall due to clean non-linear relationships in our feature set.
- **Logistic Regression:** Provided a strong linear baseline with solid interpretability.

## Recommendation for Production
XGBoost and Random Forest are selected as primary candidate models for integration into our dynamic risk engine due to their robustness against edge-case anomalies.
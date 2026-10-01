# Final Hyperparameters & Optimization Report

## Optimization Strategy
- **Algorithm:** XGBoost Classifier
- **Search Method:** RandomizedSearchCV (5-Fold Cross-Validation)
- **Optimization Metric:** F1-Score

## Final Selected Hyperparameters
- `n_estimators`: 100 / 200
- `max_depth`: 5 / 7
- `learning_rate`: 0.1
- `subsample`: 0.8
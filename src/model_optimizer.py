"""
Model Hyperparameter Tuning and Optimization Script
Tunes an XGBoost classifier using RandomizedSearchCV and saves the best production model.
"""

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score

def optimize_model(input_path="data/processed/featured_data.csv"):
    print(f"[INFO] Loading featured data from {input_path}...")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Featured data not found at {input_path}. Please complete Phase 5 first.")
        
    df = pd.read_csv(input_path)
    
    # Target definition
    df['is_high_risk'] = (df['risk_score'] > 50).astype(int)
    
    exclude_cols = ['timestamp', 'segment_id', 'road_type', 'risk_score', 'is_high_risk']
    feature_cols = [col for col in df.select_dtypes(include=[np.number]).columns if col not in exclude_cols]
    
    X = df[feature_cols]
    y = df['is_high_risk']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Feature Scaling for robust training
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define hyperparameter grid for XGBoost
    param_distributions = {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 5, 7, 10],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }
    
    base_model = XGBClassifier(random_state=42, eval_metric='logloss')
    
    print("[INFO] Running Randomized Search Cross-Validation for Hyperparameter Tuning...")
    random_search = RandomizedSearchCV(
        estimator=base_model,
        param_distributions=param_distributions,
        n_iter=10,
        cv=5,
        scoring='f1',
        random_state=42,
        n_jobs=-1
    )
    
    random_search.fit(X_train_scaled, y_train)
    
    best_model = random_search.best_estimator_
    print(f"\n[SUCCESS] Best Hyperparameters Found:\n{random_search.best_params_}")
    
    # Evaluate optimized model
    y_pred = best_model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"Optimized Model Test Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))
    
    # Save final model and feature scaler to disk
    os.makedirs("models", exist_ok=True)
    joblib.dump(best_model, "models/final_risk_model.joblib")
    joblib.dump(scaler, "models/feature_scaler.joblib")
    print("[SUCCESS] Final production model and feature scaler saved successfully in 'models/'!")

if __name__ == "__main__":
    optimize_model()
"""
Baseline Machine Learning Models Training Script
Trains Logistic Regression, Random Forest, and XGBoost classifiers for risk prediction.
"""

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_baseline_models(input_path="data/processed/featured_data.csv"):
    print(f"[INFO] Loading featured data from {input_path}...")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Featured data not found at {input_path}. Please complete Phase 5 first.")
        
    df = pd.read_csv(input_path)
    
    # Create binary target for classification: High Risk (1) if risk_score > 50 else Low Risk (0)
    df['is_high_risk'] = (df['risk_score'] > 50).astype(int)
    
    # Select feature columns (exclude non-numeric metadata and targets)
    exclude_cols = ['timestamp', 'segment_id', 'road_type', 'risk_score', 'is_high_risk']
    feature_cols = [col for col in df.select_dtypes(include=[np.number]).columns if col not in exclude_cols]
    
    X = df[feature_cols]
    y = df['is_high_risk']
    
    # Train-test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    os.makedirs("models", exist_ok=True)
    
    models = {
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
        "random_forest": RandomForestClassifier(n_estimators=50, random_state=42),
        "xgboost": XGBClassifier(n_estimators=50, random_state=42, eval_metric='logloss')
    }
    
    results = {}
    for name, model in models.items():
        print(f"\n[INFO] Training baseline {name}...")
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        results[name] = acc
        
        print(f"-> {name} Accuracy: {acc:.4f}")
        print(classification_report(y_test, y_pred))
        
        # Save trained model to disk
        model_path = f"models/baseline_{name}.joblib"
        joblib.dump(model, model_path)
        print(f"-> Saved model to {model_path}")
        
    print("\n[SUCCESS] All baseline models trained and saved successfully!")
    return results

if __name__ == "__main__":
    train_baseline_models()
"""
Data Cleaner Pipeline for Traffic Risk Dataset
Handles missing values, duplicate checks, outlier removal, and data type validation.
"""

import os
import pandas as pd
import numpy as np

def clean_traffic_data(input_path="data/raw/synthetic_traffic_data.csv", output_path="data/processed/cleaned_data.csv"):
    print(f"[INFO] Loading raw data from {input_path}...")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Raw data file not found at {input_path}. Please complete Phase 2 first.")
        
    df = pd.read_csv(input_path)
    initial_count = len(df)
    print(f"Initial row count: {initial_count}")
    
    # 1. Drop duplicate rows if any exist
    df = df.drop_duplicates()
    print(f"Rows after removing duplicates: {len(df)}")
    
    # 2. Handle missing values (Impute or drop)
    # For numerical columns, fill missing with median; for categorical, fill with mode
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"Imputed missing values in '{col}' with median: {median_val}")
            
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            df[col].fillna(mode_val, inplace=True)
            print(f"Imputed missing values in '{col}' with mode: {mode_val}")

    # 3. Outlier handling / Range validation
    # Ensure physical limits are respected (e.g., speed >= 0, congestion between 0 and 1)
    df['congestion_level'] = df['congestion_level'].clip(0.0, 1.0)
    df['risk_score'] = df['risk_score'].clip(0.0, 100.0)
    df['average_speed'] = df['average_speed'].clip(lower=0.0)
    
    # Remove rows where vehicle count or speed limits are nonsensical
    df = df[(df['vehicle_count'] >= 0) & (df['speed_limit'] > 0)]
    
    # 4. Ensure correct data types
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
    # Ensure processed folder exists and save cleaned data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"[SUCCESS] Cleaned data saved to {output_path}")
    print(f"Final row count after cleaning: {len(df)} (Removed {initial_count - len(df)} anomalous rows)")
    return df

if __name__ == "__main__":
    clean_traffic_data()
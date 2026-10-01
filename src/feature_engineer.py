"""
Feature Engineering Pipeline for Traffic Risk Dataset
Creates advanced traffic, weather, road, and temporal features for ML training.
"""

import os
import pandas as pd
import numpy as np

def engineer_features(input_path="data/processed/cleaned_data.csv", output_path="data/processed/featured_data.csv"):
    print(f"[INFO] Loading cleaned data from {input_path}...")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Cleaned data file not found at {input_path}. Please complete Phase 4 first.")
        
    df = pd.read_csv(input_path)
    
    # 1. Traffic Features: Speed Ratio (observed speed vs legal speed limit)
    # Lower ratio means heavy slowdowns or congestion relative to speed limit
    df['speed_ratio'] = df['average_speed'] / df['speed_limit'].replace(0, 1)
    df['speed_ratio'] = df['speed_ratio'].clip(0.1, 2.0)
    
    # Traffic pressure index
    df['traffic_pressure'] = df['congestion_level'] * (df['vehicle_count'] / 100.0)
    
    # 2. Weather Risk Features: Combined visibility & rainfall hazard
    # Low visibility (<200m) + heavy rain increases risk exponentially
    df['weather_hazard_score'] = np.where(
        (df['rainfall_mm'] > 20) & (df['visibility_m'] < 200), 
        80.0, 
        np.where(df['rainfall_mm'] > 10, 40.0, 10.0)
    )
    
    # 3. Road Infrastructure Risk Factor
    # Combines potholes and waterlogging status
    df['infrastructure_risk'] = (df['pothole_count'] * 2.5) + (df['waterlogging'] * 30.0)
    
    # 4. Temporal Features
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    # Save featured dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"[SUCCESS] Featured data successfully saved to {output_path}")
    print(f"Total features now available: {len(df.columns)}")
    return df

if __name__ == "__main__":
    engineer_features()
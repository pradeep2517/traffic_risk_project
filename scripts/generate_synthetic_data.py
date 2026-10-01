"""
Synthetic Traffic Data Generator for Indian Roads
Generates a CSV file containing realistic traffic, weather, road condition,
and computed risk scores for baseline model training.
"""

import os
import numpy as np
import pandas as pd

def generate_traffic_data(num_rows=1000, random_seed=42):
    np.random.seed(random_seed)
    
    timestamps = pd.date_range(start="2026-01-01 00:00:00", periods=num_rows, freq="h")
    segment_ids = [f"SEG_{np.random.randint(1, 20):03d}" for _ in range(num_rows)]
    road_types = np.random.choice(["highway", "city_road", "expressway", "rural"], size=num_rows, p=[0.3, 0.4, 0.2, 0.1])
    
    speed_limits = []
    for rt in road_types:
        if rt == "expressway":
            speed_limits.append(100)
        elif rt == "highway":
            speed_limits.append(80)
        elif rt == "city_road":
            speed_limits.append(50)
        else:
            speed_limits.append(40)
            
    vehicle_count = np.random.randint(20, 400, size=num_rows)
    congestion_level = np.round(vehicle_count / 400.0 + np.random.normal(0, 0.05, num_rows), 2)
    congestion_level = np.clip(congestion_level, 0.0, 1.0)
    
    # Average speed inversely related to congestion
    average_speed = np.array([
        max(10, sl * (1 - cl) + np.random.normal(0, 5))
        for sl, cl in zip(speed_limits, congestion_level)
    ])
    average_speed = np.round(average_speed, 2)
    
    rainfall_mm = np.random.choice([0.0, np.random.uniform(1.0, 80.0)], size=num_rows, p=[0.7, 0.3])
    visibility_m = np.where(rainfall_mm > 20, np.random.uniform(50, 200), np.random.uniform(800, 5000))
    visibility_m = np.round(visibility_m, 2)
    
    pothole_count = np.random.poisson(lam=3, size=num_rows)
    waterlogging = np.where(rainfall_mm > 30, np.random.choice([0, 1], size=num_rows, p=[0.4, 0.6]), 0)
    sudden_braking_events = np.random.poisson(lam=2, size=num_rows)
    
    hours = timestamps.hour
    is_peak_hour = np.where(((hours >= 8) & (hours <= 11)) | ((hours >= 17) & (hours <= 20)), 1, 0)
    
    # Compute heuristic risk score (0-100) for baseline target
    risk_scores = []
    for i in range(num_rows):
        r_cong = congestion_level[i] * 35
        r_rain = min(rainfall_mm[i] / 80.0 * 20, 20)
        r_pothole = min(pothole_count[i] * 2, 15)
        r_water = waterlogging[i] * 15
        r_brake = min(sudden_braking_events[i] * 3, 15)
        
        total_risk = r_cong + r_rain + r_pothole + r_water + r_brake
        risk_scores.append(min(round(total_risk + np.random.normal(0, 3), 2), 100.0))
        
    df = pd.DataFrame({
        "timestamp": timestamps,
        "segment_id": segment_ids,
        "road_type": road_types,
        "speed_limit": speed_limits,
        "vehicle_count": vehicle_count,
        "congestion_level": congestion_level,
        "average_speed": average_speed,
        "rainfall_mm": rainfall_mm,
        "visibility_m": visibility_m,
        "pothole_count": pothole_count,
        "waterlogging": waterlogging,
        "sudden_braking_events": sudden_braking_events,
        "hour_of_day": hours,
        "is_peak_hour": is_peak_hour,
        "risk_score": risk_scores
    })
    
    os.makedirs("data/raw", exist_ok=True)
    output_path = "data/raw/synthetic_traffic_data.csv"
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Synthetic dataset generated successfully at: {output_path}")
    print(f"Total rows generated: {len(df)}")

if __name__ == "__main__":
    generate_traffic_data()
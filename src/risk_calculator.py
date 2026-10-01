"""
Dynamic Risk-Score Engine for Traffic Accident Prevention
Computes a normalized 0-100 risk score based on ML probability and weighted situational factors.
"""

import numpy as np

class RiskCalculator:
    def __init__(self):
        # Weight distribution for composite risk score formula
        self.w_ml = 0.40
        self.w_traffic = 0.20
        self.w_weather = 0.15
        self.w_road = 0.15
        self.w_behavior = 0.10

    def compute_risk(self, ml_probability, congestion_level, rainfall_mm, pothole_count, waterlogging, sudden_braking_events):
        """
        Computes dynamic risk score (0-100) and classifies risk level.
        """
        # 1. ML Component (0 to 100 scale)
        r_ml = float(ml_probability) * 100.0
        
        # 2. Traffic Component (congestion level 0-1 scaled to 0-100)
        r_traffic = float(congestion_level) * 100.0
        
        # 3. Weather Component (rainfall scaled, capped at 100)
        r_weather = min((float(rainfall_mm) / 80.0) * 100.0, 100.0)
        
        # 4. Road Condition Component (potholes + waterlogging status)
        r_road = min((int(pothole_count) * 3.0) + (float(waterlogging) * 50.0), 100.0)
        
        # 5. Vehicle Behavior Component (sudden braking instances scaled)
        r_behavior = min((int(sudden_braking_events) / 10.0) * 100.0, 100.0)
        
        # Weighted Composite Score Formula
        composite_score = (
            (r_ml * self.w_ml) +
            (r_traffic * self.w_traffic) +
            (r_weather * self.w_weather) +
            (r_road * self.w_road) +
            (r_behavior * self.w_behavior)
        )
        
        final_score = round(min(max(composite_score, 0.0), 100.0), 2)
        risk_level = self.classify_risk_level(final_score)
        
        return {
            "risk_score": final_score,
            "risk_level": risk_level,
            "breakdown": {
                "ml_risk": round(r_ml, 2),
                "traffic_risk": round(r_traffic, 2),
                "weather_risk": round(r_weather, 2),
                "road_risk": round(r_road, 2),
                "behavior_risk": round(r_behavior, 2)
            }
        }

    def classify_risk_level(self, score):
        if score <= 25:
            return "LOW (Green)"
        elif score <= 50:
            return "MODERATE (Yellow)"
        elif score <= 75:
            return "HIGH (Orange)"
        else:
            return "CRITICAL (Red)"

if __name__ == "__main__":
    calc = RiskCalculator()
    sample_result = calc.compute_risk(
        ml_probability=0.75, 
        congestion_level=0.85, 
        rainfall_mm=45.0, 
        pothole_count=4, 
        waterlogging=1, 
        sudden_braking_events=3
    )
    print("[SUCCESS] Risk Calculator Test Result:")
    print(sample_result)
"""
Unified Simulation Runner
Combines traffic, weather, and road condition generators into a single test loop.
"""

import sys
import os
import time
import random
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

API_URL = "http://127.0.0.1:8000/api/predict-risk"

def run_live_simulation(ticks=5):
    print(f"[INFO] Starting live simulation against API endpoint: {API_URL}")
    print("[INFO] Make sure your FastAPI server is running (python -m uvicorn api.main:app --reload)\n")
    
    for i in range(ticks):
        # Simulate varying environmental parameters
        payload = {
            "speed_limit": 80,
            "average_speed": round(random.uniform(20.0, 75.0), 2),
            "congestion_level": round(random.uniform(0.3, 0.95), 2),
            "rainfall_mm": round(random.uniform(0.0, 60.0), 2),
            "visibility_m": round(random.uniform(50.0, 1000.0), 2),
            "pothole_count": random.randint(0, 15),
            "waterlogging": random.choice([0, 1]),
            "sudden_braking_events": random.randint(0, 6)
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"[Tick {i+1}] Risk Score: {data['risk_score']} / 100 | Level: {data['risk_level']}")
            else:
                print(f"[Tick {i+1}] API Error: {response.text}")
        except requests.exceptions.ConnectionError:
            print("[ERROR] Could not connect to FastAPI server. Is it running on port 8000?")
            break
            
        time.sleep(1.5)

if __name__ == "__main__":
    run_live_simulation()
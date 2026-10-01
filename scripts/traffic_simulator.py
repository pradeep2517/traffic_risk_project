"""
Real-Time Traffic Data Simulator
Generates fluctuating vehicle counts, congestion levels, and speeds for road segments.
"""

import time
import random
import datetime

def simulate_traffic_stream(segment_id="SEG_001"):
    print(f"[SIMULATOR] Starting live traffic data stream for {segment_id}...")
    try:
        for _ in range(5):  # Simulate 5 live ticks for demonstration
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            vehicle_count = random.randint(50, 350)
            congestion_level = round(vehicle_count / 400.0, 2)
            average_speed = round(max(15.0, 80.0 * (1 - congestion_level) + random.uniform(-5, 5)), 2)
            sudden_braking = random.choices([0, 1, 2, 3], weights=[0.6, 0.2, 0.1, 0.1])[0]
            
            reading = {
                "timestamp": timestamp,
                "segment_id": segment_id,
                "vehicle_count": vehicle_count,
                "congestion_level": congestion_level,
                "average_speed": average_speed,
                "sudden_braking_events": sudden_braking
            }
            
            print(f"[{timestamp}] Traffic Reading -> Congestion: {int(congestion_level*100)}% | Speed: {average_speed} km/h | Braking Events: {sudden_braking}")
            time.sleep(1) # 1 second delay between telemetry ticks
            
    except KeyboardInterrupt:
        print("[SIMULATOR] Traffic stream stopped by user.")

if __name__ == "__main__":
    simulate_traffic_stream()
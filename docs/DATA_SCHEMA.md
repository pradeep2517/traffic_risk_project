# Traffic Risk Dataset Schema

| Column Name | Data Type | Description | Range / Values |
| :--- | :--- | :--- | :--- |
| `timestamp` | Datetime | Time of reading | YYYY-MM-DD HH:MM:SS |
| `segment_id` | String | Unique road segment identifier | e.g., `SEG_001` |
| `road_type` | Categorical | Type of road infrastructure | `highway`, `city_road`, `expressway`, `rural` |
| `speed_limit` | Integer | Legal speed limit (km/h) | 30 - 120 |
| `vehicle_count` | Integer | Number of vehicles detected in frame/interval | 10 - 500 |
| `congestion_level` | Float | Traffic congestion percentage | 0.0 - 1.0 (0% to 100%) |
| `average_speed` | Float | Average observed speed (km/h) | 5.0 - 120.0 |
| `rainfall_mm` | Float | Rainfall intensity | 0.0 - 150.0 mm |
| `visibility_m` | Float | Atmospheric visibility | 20.0 - 5000.0 meters |
| `pothole_count` | Integer | Number of detected potholes in segment | 0 - 50 |
| `waterlogging` | Integer | Waterlogging status | 0 (No), 1 (Yes) |
| `sudden_braking_events`| Integer | Count of abrupt braking instances | 0 - 20 |
| `hour_of_day` | Integer | Hour component | 0 - 23 |
| `is_peak_hour` | Integer | Peak traffic indicator | 0 (No), 1 (Yes) |
| `risk_score` | Float | Calculated composite risk score | 0.0 - 100.0 |
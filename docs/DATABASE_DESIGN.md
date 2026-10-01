# Database Design Documentation

## Overview
We utilize SQLAlchemy ORM with SQLite for local development and rapid prototyping, easily scalable to PostgreSQL for production deployment.

## Key Tables
1. **`road_segments`**: Stores static infrastructure data (latitude, longitude, speed limit, road type).
2. **`risk_predictions`**: Logs real-time computed risk scores, levels, and factor breakdowns.
3. **`alerts`**: Tracks active early warning messages generated for drivers and authorities.
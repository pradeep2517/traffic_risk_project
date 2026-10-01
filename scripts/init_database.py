"""
Database Initialization Script
Creates all defined tables inside the SQLite/PostgreSQL database.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import engine, Base
from src.models_db import RoadSegmentModel, RiskPredictionLogModel, AlertModel

def init_db():
    print("[INFO] Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("[SUCCESS] Database tables created successfully in data/traffic_risk.db!")

if __name__ == "__main__":
    init_db()
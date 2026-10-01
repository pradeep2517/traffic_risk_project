"""
SQLAlchemy ORM Models for Road Segments, Readings, Risk Predictions, and Alerts
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, JSON
from src.database import Base

class RoadSegmentModel(Base):
    __tablename__ = "road_segments"
    
    segment_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    location_id = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    road_name = Column(String, nullable=False)
    road_type = Column(String, nullable=False)
    speed_limit = Column(Integer, nullable=False)
    length_km = Column(Float, nullable=False)
    infrastructure_rating = Column(Float, default=5.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class RiskPredictionLogModel(Base):
    __tablename__ = "risk_predictions"
    
    prediction_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    segment_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    contributing_factors = Column(JSON, nullable=True)
    model_version = Column(String, default="1.0.0")

class AlertModel(Base):
    __tablename__ = "alerts"
    
    alert_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    segment_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    risk_level = Column(String, nullable=False)
    alert_message = Column(String, nullable=False)
    language = Column(String, default="en")
    read = Column(Boolean, default=False)
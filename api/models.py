"""
Pydantic Data Models for FastAPI Request and Response Validation
"""

from pydantic import BaseModel, Field

class RiskPredictionRequest(BaseModel):
    congestion_level: float = Field(..., ge=0.0, le=1.0, description="Traffic congestion level (0.0 to 1.0)")
    average_speed: float = Field(..., ge=0.0, description="Average speed in km/h")
    speed_limit: float = Field(..., gt=0.0, description="Legal speed limit in km/h")
    rainfall_mm: float = Field(..., ge=0.0, description="Rainfall intensity in mm")
    visibility_m: float = Field(..., ge=0.0, description="Visibility in meters")
    pothole_count: int = Field(..., ge=0, description="Number of potholes detected")
    waterlogging: int = Field(..., ge=0, le=1, description="Waterlogging status (0 or 1)")
    sudden_braking_events: int = Field(..., ge=0, description="Count of sudden braking events")

class RiskPredictionResponse(BaseModel):
    risk_score: float
    risk_level: str
    ml_probability: float
    breakdown: dict
"""
API Routes for Risk Prediction and Health Checks with Database Logging
"""

import os
import joblib
import numpy as np
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.models import RiskPredictionRequest, RiskPredictionResponse
from src.risk_calculator import RiskCalculator
from src.database import get_db
from src.models_db import RiskPredictionLogModel

router = APIRouter()

# Load trained model, scaler, and risk calculator on startup
MODEL_PATH = "models/final_risk_model.joblib"
SCALER_PATH = "models/feature_scaler.joblib"

model = None
scaler = None

if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("[INFO] Production model and scaler loaded into API successfully.")
else:
    print("[WARNING] Trained model files not found. Please complete Phase 9 first.")

risk_engine = RiskCalculator()

@router.get("/health", summary="Health Check")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@router.post("/api/predict-risk", response_model=RiskPredictionResponse, summary="Predict Road Risk Score & Log to DB")
def predict_risk(payload: RiskPredictionRequest, db: Session = Depends(get_db)):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="ML Model not loaded on server. Run Phase 9 first.")
        
    try:
        speed_ratio = payload.average_speed / max(payload.speed_limit, 1)
        traffic_pressure = payload.congestion_level * 2.0
        weather_hazard = 80.0 if (payload.rainfall_mm > 20 and payload.visibility_m < 200) else (40.0 if payload.rainfall_mm > 10 else 10.0)
        infra_risk = (payload.pothole_count * 2.5) + (payload.waterlogging * 30.0)
        
        feature_vector = np.array([[
            payload.speed_limit,
            200,
            payload.congestion_level,
            payload.average_speed,
            payload.rainfall_mm,
            payload.visibility_m,
            payload.pothole_count,
            payload.waterlogging,
            payload.sudden_braking_events,
            12, 1, speed_ratio, traffic_pressure, weather_hazard, infra_risk, 2, 0
        ]])
        
        scaled_features = scaler.transform(feature_vector)
        ml_prob = float(model.predict_proba(scaled_features)[0][1])
        
        # Compute composite risk score
        result = risk_engine.compute_risk(
            ml_probability=ml_prob,
            congestion_level=payload.congestion_level,
            rainfall_mm=payload.rainfall_mm,
            pothole_count=payload.pothole_count,
            waterlogging=payload.waterlogging,
            sudden_braking_events=payload.sudden_braking_events
        )
        
        # Save prediction log to SQLite database
        db_log = RiskPredictionLogModel(
            segment_id="SEG_001",
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            contributing_factors=result["breakdown"],
            model_version="1.0.0"
        )
        db.add(db_log)
        db.commit()
        
        return {
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "ml_probability": round(ml_prob, 4),
            "breakdown": result["breakdown"]
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
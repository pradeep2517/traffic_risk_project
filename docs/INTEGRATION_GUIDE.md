# System Integration Guide

## Overview
Phase 14 connects all system layers into a unified pipeline:
1. **Frontend UI (`static/index.html`):** Captures user/sensor parameters via interactive sliders.
2. **FastAPI Backend (`api/routes.py`):** Receives HTTP POST requests, scales inputs, and queries the trained XGBoost model (`models/final_risk_model.joblib`).
3. **Risk Engine (`src/risk_calculator.py`):** Calculates composite 0-100 risk score and tier breakdown.
4. **Database Logging (`data/traffic_risk.db`):** Automatically logs every prediction event for audit trails and historical analysis.
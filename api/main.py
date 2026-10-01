"""
Main FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router

app = FastAPI(
    title="Smart Traffic Accident Risk Detection API",
    description="Real-time dynamic risk estimation and early warning API for Indian roads.",
    version="1.0.0"
)

# Include API routes
app.include_router(router)

# Mount the static folder so FastAPI serves your HTML frontend at http://127.0.0.1:8000
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
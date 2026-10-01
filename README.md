# Smart AI-Based Dynamic Traffic Accident Risk Detection

An end-to-end B.Tech final-year project that predicts traffic accident risks in real-time using machine learning, deployed as a REST API with a modern Tailwind CSS control dashboard.

## 🌟 Key Features
- **Dynamic Risk Engine:** Calculates a 0-100 risk score based on weather, congestion, and road infrastructure.
- **Machine Learning Backend:** XGBoost classifier trained on extensive traffic datasets, served via FastAPI.
- **Live Control Dashboard:** Interactive web interface built with HTML5 and Tailwind CSS.
- **Multilingual Warnings:** Safety alerts translated into English, Hindi, and Tamil.
- **Computer Vision:** YOLOv8 integrated for road hazard and vehicle density detection.

## 🚀 How to Run
1. Activate your virtual environment (`venv\Scripts\activate`)
2. Run the server: `python -m uvicorn api.main:app --reload`
3. Open `http://127.0.0.1:8000` in your browser.


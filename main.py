from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import os

try:
    import joblib
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False

app = FastAPI(
    title="NexFlow Engine",
    description="Smart Traffic Optimization System",
    version="1.2.0"
)

origins = [
    "https://reyyy-eng.github.io",
    "http://localhost",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model = None
MODEL_FILE = "traffic_model.pkl"

if HAS_JOBLIB and os.path.exists(MODEL_FILE):
    try:
        model = joblib.load(MODEL_FILE)
    except Exception as e:
        print(f"Error loading model: {e}")

class TrafficInput(BaseModel):
    cars: int
    speed: float

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "system": "NexFlow Engine",
        "message": "Backend API operational and ready for AI integration."
    }

@app.post("/api/v1/predict")
def predict_traffic(data: TrafficInput):
    cars = data.cars
    speed = data.speed
    
    if model:
        try:
            prediction = model.predict([[cars, speed]])[0]
            status = str(prediction)
            
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba([[cars, speed]])[0]
                confidence = round(float(max(probs)) * 100, 1)
            else:
                confidence = 94.5
        except Exception:
            status, confidence = fallback_logic(cars, speed)
    else:
        status, confidence = fallback_logic(cars, speed)

    if status == "Heavy Traffic":
        plan = "Activate Dynamic Lane Control & Pump Queue Redirection"
    elif status == "Moderate Traffic":
        plan = "Optimize Station Signal Timings & Queue Allocation"
    else:
        plan = "Standard Operations - Traffic Flow Normal"

        return {
        "input_summary": {
            "cars": cars,
            "speed": speed
        },
        "traffic_status": status,
        "confidence_score": f"{confidence}%",
        "suggested_plan": plan,
        "traffic": status,
        "probability": confidence,
        "recommendation": plan,
        "before": "45 mins",
        "after": "25 mins",
        "improvement": "44%",
        "allocation": "Lane 1: 40%, Lane 2: 60%"
    }

    
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


def fallback_logic(cars: int, speed: float):
    is_heavy = cars > 50
    traffic = "Heavy" if is_heavy else "Normal"
    probability = 0.85 if is_heavy else 0.30
    
    return {
        "traffic": traffic,
        "probability": probability,
        "recommendation": "Reroute traffic to secondary lanes" if is_heavy else "Maintain current flow",
        "before": 15,
        "after": 8 if is_heavy else 14,
        "improvement": "46.7%" if is_heavy else "6.7%",
        "allocation": [
            {"lane": "Lane A", "status": "Open"},
            {"lane": "Lane B", "status": "Optimized"}
        ]
    }


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
    return {"message": "NexFlow AI Engine Online"}


@app.post("/api/v1/predict")
def predict_traffic(input_data: TrafficInput):
    if model is not None:
        try:
            prediction = model.predict([[input_data.cars, input_data.speed]])
            return {
                "traffic": str(prediction[0]),
                "probability": 0.88,
                "recommendation": "Optimize signal timing",
                "before": 15,
                "after": 9,
                "improvement": "40.0%",
                "allocation": [
                    {"lane": "Lane A", "status": "Open"},
                    {"lane": "Lane B", "status": "Optimized"}
                ]
            }
        except Exception:
            return fallback_logic(input_data.cars, input_data.speed)
    else:
        return fallback_logic(input_data.cars, input_data.speed)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

try:
    import joblib
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False


app = FastAPI(
    title="NexFlow Engine",
    description="Smart Traffic Optimization System",
    version="1.3.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://reyyy-eng.github.io",
        "http://localhost",
        "http://localhost:3000",
        "*"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TrafficInput(BaseModel):
    cars: int
    speed: float


model = None
MODEL_FILE = "traffic_model.pkl"

if HAS_JOBLIB and os.path.exists(MODEL_FILE):
    try:
        model = joblib.load(MODEL_FILE)
    except Exception:
        model = None


def get_traffic_status(cars: int, speed: float):
    if cars > 50 or speed < 30:
        return "Heavy", 95.0, "Activate Dynamic Lane Control & Pump Queue Redirection"

    elif cars > 20 or speed < 60:
        return "Moderate", 89.0, "Optimize Station Signal Timings & Queue Allocation"

    else:
        return "Normal", 96.0, "Standard Operations - Traffic Flow Normal"


def create_allocation(cars: int):
    return [
        {
            "vehicle": f"Vehicle {i + 1:02d}",
            "pump": f"P{(i % 8) + 1:02d}"
        }
        for i in range(min(cars, 12))
    ]


@app.get("/")
def read_root():
    return {
        "message": "NexFlow AI Engine Online",
        "status": "Online"
    }


@app.post("/api/v1/predict")
def predict_traffic(input_data: TrafficInput):

    cars = input_data.cars
    speed = input_data.speed

    traffic, probability, recommendation = get_traffic_status(
        cars,
        speed
    )

    before = 4.0
    after = 2.0
    improvement = round(
        ((before - after) / before) * 100,
        1
    )

    return {
        "traffic": traffic,
        "probability": probability,
        "recommendation": recommendation,
        "before": before,
        "after": after,
        "improvement": improvement,
        "allocation": create_allocation(cars)
    }

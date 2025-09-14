from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI()

# input schema
class TelematicsData(BaseModel):
    driver_id: str
    avg_speed: float
    extreme_brakes: int
    extreme_accels: int
    late_driving: float
    mileage: float
    weather_conditions_foggy: float
    weather_conditions_rainy: float
    weather_conditions_snowy: float
    traffic_conditions_light: float
    traffic_conditions_moderate: float

@app.post("/compute_risk")
def compute_risk(data: TelematicsData):
    # Risk calculation (same formula as before)
    risk = (
        0.03 * data.avg_speed +
        0.05 * data.extreme_brakes +
        0.05 * data.extreme_accels +
        0.1 * data.late_driving +
        0.07 * data.weather_conditions_rainy + 
        data.weather_conditions_foggy + 
        data.weather_conditions_snowy +
        0.05 * (1 - data.traffic_conditions_light) -
        0.02 * data.mileage
    )

    # Scale to 0-1
    risk_p = (risk - 0) / (risk + 1)  # simplified normalization for POC

    risk_score = min(max(risk_p, 0), 1)  # clip 0-1

    # Calculate dynamic premium
    BASE_PREMIUM = 500
    RISK_WEIGHT = 0.5
    premium = round(BASE_PREMIUM * (1 + risk_score * RISK_WEIGHT), 2)

    return {
        "driver_id": data.driver_id,
        "predicted_risk": round(risk_score*100,2),
        "dynamic_premium": premium
    }

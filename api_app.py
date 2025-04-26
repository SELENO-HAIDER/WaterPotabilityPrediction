# api_app.py
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib

model = joblib.load('water_potability_model.pkl')
scaler = joblib.load('scaler.pkl')

app = FastAPI()

class InputData(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float
    hardness_ph_interaction: float
    hardness_Chloramines_Interaction: float
    hardness_Chloramines_Sum: float
    hardness_Chloramines_Difference: float
    neutral: int
    basic: int

@app.post("/predict")
def predict(data: InputData):
    features = np.array([[data.ph, data.Hardness, data.Solids, data.Chloramines, data.Sulfate,
                          data.Conductivity, data.Organic_carbon, data.Trihalomethanes, data.Turbidity,
                          data.hardness_ph_interaction, data.hardness_Chloramines_Interaction,
                          data.hardness_Chloramines_Sum, data.hardness_Chloramines_Difference,
                          data.neutral, data.basic]])
    
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)
    return {"prediction": int(prediction[0])}

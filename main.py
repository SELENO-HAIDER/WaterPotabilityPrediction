from fastapi import FastAPI
import joblib
import pandas as pd
import numpy as np
from pydantic import BaseModel

model = joblib.load("water_potability_model.pkl")
feature_columns = [
    "ph", "Hardness", "Solids", "Chloramines", 
    "Sulfate", "Conductivity", "Organic_carbon", 
    "Trihalomethanes", "Turbidity"
]

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

def predict(new_data: dict):
    df = pd.DataFrame([new_data])
    df = df.reindex(columns=feature_columns, fill_value=0)
    prediction = model.predict(df)
    return int(prediction[0])

@app.post("/predict")
def get_prediction(data: InputData):
    result = predict(data.model_dump())
    potability = "Potable" if result == 1 else "Not Potable"
    return {
        "prediction": result,
        "potability": potability
    }

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

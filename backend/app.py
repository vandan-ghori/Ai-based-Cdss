from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import pandas as pd

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Since this is a prototype
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
try:
    model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
    model = joblib.load(model_path)
except Exception as e:
    model = None
    print(f"Warning: Model not loaded. {e}")

# Defining the input data structure
class MigraineFeatures(BaseModel):
    Age: int
    Duration: int
    Frequency: int
    Intensity: int
    Vomit: int
    Phonophobia: int

@app.get("/")
def read_root():
    return {"message": "Migraine Prediction API is running!"}

@app.post("/predict")
def predict_migraine(features: MigraineFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded. Please train the model first.")
    
    # Convert input to DataFrame
    input_data = pd.DataFrame([features.dict()])
    
    # Make prediction
    try:
        prediction = model.predict(input_data)
        predicted_type = str(prediction[0])
        return {"predicted_type": predicted_type}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

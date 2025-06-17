# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import os

# Define input data structure
class PatientData(BaseModel):
    age: float
    sex: float  
    bmi: float
    bp: float   # blood pressure
    s1: float   # serum measurement 1
    s2: float   # serum measurement 2  
    s3: float   # serum measurement 3
    s4: float   # serum measurement 4
    s5: float   # serum measurement 5
    s6: float   # serum measurement 6


# Initialize FastAPI app
app = FastAPI(
    title="Diabetes Progression Predictor",
    description="Predicts diabetes progression score from physiological features",
    version="1.0.0"
)
 
# Load the trained model
model_path = os.path.join("models", "diabetes_model.pkl")
with open(model_path, 'rb') as f:
    model = pickle.load(f)

#Let create the prediction endpoint
@app.post("/predict")
def predict_progression(patient: PatientData):
    """
    Predict diabetes progression score
    """
    # Convert input to numpy array
    features = np.array([[
        patient.age, patient.sex, patient.bmi, patient.bp,
        patient.s1, patient.s2, patient.s3, patient.s4,
        patient.s5, patient.s6
    ]])
    
    # Make prediction
    prediction = model.predict(features)[0]
    
    # Return result with additional context
    return {
        "predicted_progression_score": round(prediction, 2),
        "interpretation": get_interpretation(prediction)
    }
 
def get_interpretation(score):
    """Provide human-readable interpretation of the score"""
    if score < 100:
        return "Below average progression"
    elif score < 150:
        return "Average progression"
    else:
        return "Above average progression"


#Let's add a health check endpoint
@app.get("/")
def health_check():
    return {"status": "healthy", "model": "diabetes_progression_v1"}

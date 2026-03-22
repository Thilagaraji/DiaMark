

import os
import joblib


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "xgb_model.pkl")

model = joblib.load(model_path)
def load_model():
    """Load and return the trained XGBoost model"""
    model = joblib.load(model_path)
    return model

def pattern_to_numeric(pattern):
    mapping = {"Loop": 0, "Whorl": 1, "Arch": 2}
    return mapping.get(pattern, 0)

def predict_risk(model, features, bmi, age, family_history, gender):
    import numpy as np

    # Model expects 12 features: age, gender, 10 fingers (here most zeros), family_history optional
    X = np.array([
        age,
        gender,
        features["R5"], features["R4"], features["R3"], features["R2"], features["R1"],
        features["L1"], features["L2"], features["L3"], features["L4"], features["L5"]
    ]).reshape(1, -1)

    # Predict
    proba = model.predict_proba(X)[0][1]
    
    if proba < 0.33:
        risk = "LOW"
    elif proba < 0.66:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "prediction": int(model.predict(X)[0]),
        "probability": float(proba),
        "risk_level": risk
    }
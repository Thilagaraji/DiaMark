import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import joblib
import numpy as np
from fingerprint_processing.pattern_detector import detect_fingerprint_pattern

# Load trained model
model = joblib.load("xgb_model.pkl")


def encode_pattern(pattern):
    """
    Convert fingerprint pattern to numeric value
    """
    mapping = {
        "Arch": 0,
        "Loop": 1,
        "Whorl": 2
    }

    return mapping.get(pattern, 1)
def encode_gender(gender):
    if gender.lower() == "male":
        return 1
    else:
        return 0

def predict_diabetes(image_path, age, gender):
    """
    Predict diabetes risk using fingerprint pattern
    """

    # Step 1 — Detect pattern
    pattern = detect_fingerprint_pattern(image_path)

    pattern_value = encode_pattern(pattern)
    gender_value = encode_gender(gender)
    # Step 2 — Create feature vector (10 fingers)
    features = [
    age,
    gender_value,
    pattern_value, pattern_value, pattern_value, pattern_value, pattern_value,
    pattern_value, pattern_value, pattern_value, pattern_value, pattern_value
]
    features = np.array(features).reshape(1, -1)

    # Step 3 — Prediction
    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0][1]

    # Step 4 — Convert to readable result
    if probability < 0.33:
        risk = "LOW"
    elif probability < 0.66:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "pattern": pattern,
        "risk_level": risk,
        "probability": float(probability)
    }
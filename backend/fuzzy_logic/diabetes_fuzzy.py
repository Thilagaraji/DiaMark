import numpy as np

def fuzzy_risk(probability):
    """
    Convert ML probability into fuzzy diabetes risk + confidence
    """

    probability = float(probability)

    # LOW RISK
    if probability < 0.4:
        risk = "LOW"
        confidence = 1 - (probability / 0.4)

    # MEDIUM RISK
    elif 0.4 <= probability <= 0.7:
        risk = "MEDIUM"
        confidence = 1 - abs(probability - 0.55) / 0.15

    # HIGH RISK
    else:
        risk = "HIGH"
        confidence = (probability - 0.7) / 0.3

    # Clamp values between 0 and 1
    confidence = max(0, min(confidence, 1))

    return {
        "risk": risk,
        "confidence": round(confidence * 100, 2),  # convert to %
        "probability": round(probability * 100, 2)
    }
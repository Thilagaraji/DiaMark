import numpy as np


def fuzzy_risk(probability):
    """
    Convert ML probability (must be in [0, 1]) into a fuzzy
    diabetes risk level and a human-readable confidence percentage.

    Returns:
        {
            "risk":        "LOW" | "MEDIUM" | "HIGH",
            "confidence":  float  (0–100, percentage),
            "probability": float  (0–100, percentage)
        }
    """
    probability = float(np.clip(probability, 0.0, 1.0))

    if probability < 0.4:
        risk       = "LOW"
        # confidence rises as probability falls toward 0
        confidence = 1.0 - (probability / 0.4)

    elif probability <= 0.7:
        risk       = "MEDIUM"
        # confidence peaks at the centre of the medium band (0.55)
        confidence = 1.0 - abs(probability - 0.55) / 0.15

    else:
        risk       = "HIGH"
        # confidence rises as probability rises toward 1
        confidence = (probability - 0.7) / 0.3

    # Hard clamp – confidence must never exceed 100 %
    confidence = float(np.clip(confidence, 0.0, 1.0))

    return {
        "risk":        risk,
        "confidence":  round(confidence * 100, 2),   # e.g. 87.50
        "probability": round(probability * 100, 2),  # e.g. 34.20
    }
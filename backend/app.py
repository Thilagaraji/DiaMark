from flask import Flask, request, jsonify, send_from_directory
import uuid
import os
import csv
import time
from flask_cors import CORS

from fuzzy_logic.diabetes_fuzzy import fuzzy_risk
from utils.pdf_report import generate_report
from fingerprint_processing.preprocessing import preprocess_fingerprint
from fingerprint_processing.extractor import extract_features
from fingerprint_processing.pattern_detector import detect_pattern
from utils.bmi import calculate_bmi

import joblib
import numpy as np

# ✅ Load trained model + scaler
model = joblib.load("models/xgb_model.pkl")
scaler = joblib.load("models/xgb_model_scaler.pkl")

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


# ✅ ROUTE 1: PREDICT
@app.route("/predict", methods=["POST"])
def predict():
    try:
        name = request.form["name"]
        age = int(request.form["age"])
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        family_history = 1 if request.form["family_history"] == "yes" else 0
        gender = 1 if request.form["gender"] == "M" else 0

        file = request.files["fingerprint"]

        filename = str(uuid.uuid4()) + "_" + file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # ✅ Image processing
        img = preprocess_fingerprint(filepath)
        features_single = extract_features(img)

        # ✅ Pattern + BMI
        pattern = detect_pattern(img)
        bmi = calculate_bmi(height, weight)

        # ✅ ML INPUT (same as training)
        feature_array = [
            features_single["ridge_density"],
            features_single["ridge_thickness"],
            features_single["ridge_ratio"],
            features_single["minutiae_points"]
        ]

        feature_array = np.array(feature_array).reshape(1, -1)
        feature_array = scaler.transform(feature_array)

        # ✅ ML prediction
        prob = model.predict_proba(feature_array)[0][1]

        # ✅ Fuzzy logic
        fuzzy_output = fuzzy_risk(prob)

        risk = fuzzy_output["risk"]
        confidence = fuzzy_output["confidence"]
        probability = fuzzy_output["probability"]
        # ✅ Generate PDF report
        report_file = generate_report(
    name,
    age,
    bmi,
    pattern,
    risk,
    probability,
    REPORT_FOLDER
)
        response = {
      "risk_level": risk,
      "confidence": confidence,
      "probability": probability,
      "pattern": pattern,
      "report_path": f"reports/{report_file}"
}

        # ✅ CSV LOGGING
        log_file = "prediction_log.csv"
        file_exists = os.path.isfile(log_file)

        with open(log_file, "a", newline="") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow([
                    "timestamp", "name", "age", "bmi",
                    "risk_level", "probability"
                ])

            writer.writerow([
                int(time.time()),
                name,
                age,
                round(bmi, 2),
                risk,
                probability
            ])

        print("✅ RESPONSE:", response)
        return jsonify(response)

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"message": str(e)}), 500


# ✅ ROUTE 2: SERVE PDF
@app.route('/reports/<path:filename>')
def download_report(filename):
    try:
        return send_from_directory(REPORT_FOLDER, filename)
    except Exception:
        return jsonify({"error": "File not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
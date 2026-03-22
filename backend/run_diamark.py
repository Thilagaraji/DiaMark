import sys
import os
import cv2
import csv
from PIL import Image
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fingerprint_processing.preprocessing import preprocess_fingerprint
from fingerprint_processing.extractor import extract_features
from models.predict import model, predict_risk
from utils.bmi import calculate_bmi, bmi_category
from report.report_generator import generate_report

def main():
    print("Welcome to DiaMark Diabetes Risk Assessment\n")

    # Step 1: Get user info
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    gender_input = input("Enter Gender (M/F): ").strip().upper()
    gender = 1 if gender_input == 'M' else 0

    while True:
     try:
        height = float(input("Enter Height (cm or meters): "))
        weight = float(input("Enter Weight in kg: "))

        if height <= 0 or weight <= 0:
            print("❌ Height and weight must be positive.")
            continue

        break

     except ValueError:
        print("❌ Please enter valid numbers.")
    bmi = calculate_bmi(height, weight)
    bmi_cat = bmi_category(bmi)

    family_history_input = input("Family history of diabetes? (Yes/No): ").strip().lower()
    family_history = 1 if family_history_input in ['yes', 'y'] else 0

    # Step 2: Get fingerprint image
    

    while True:
      image_path = input("Enter fingerprint image path: ")

      if not os.path.exists(image_path):
        print("❌ File not found. Please try again.")
        continue

      try:
         Image.open(image_path)
         break
      except:
        print("❌ File is not a valid image.")

    # Step 3: Preprocess and extract features from single fingerprint
    preprocessed_img = preprocess_fingerprint(image_path)
    features_single = extract_features(preprocessed_img)

# Check if feature extraction failed
    if not features_single or "ridge_density" not in features_single:
      print("❌ Unable to extract fingerprint features. Please try another image.")
      return

# Step 4: Fill all 12 features expected by the model
    features = {
    "R5": 0, "R4": 0, "R3": 0, "R2": 0,
    "R1": features_single["ridge_density"],
    "L1": 0, "L2": 0, "L3": 0, "L4": 0, "L5": 0
}

    # Step 5: Predict risk
    prediction = predict_risk(model, features, bmi, age, family_history, gender)

    print("\n==============================")
    print("      Diabetes Risk Result")
    print("==============================")

    print("Risk Level        :", prediction["risk_level"])
    print("Model Confidence  :", round(prediction["probability"] * 100, 2), "%")

    print("==============================\n")

    # Step 6: Generate report
    report_data = {
        "name": name,
        "age": age,
        "gender": gender_input,
        "bmi": round(bmi, 2),
        "bmi_category": bmi_cat,
        "pattern": "Thumb (Right)",  # since single finger
        "risk_level": prediction["risk_level"],
        "probability": round(prediction["probability"], 2),
        "explanation": ["Based on fingerprint analysis, BMI, age, and family history."],
        "recommendations": [
            "Maintain healthy diet",
            "Exercise regularly",
            "Monitor blood sugar",
            "Consult a doctor if necessary"
        ]
    }

    generate_report(report_data)
    # Save prediction log
    log_file = "prediction_log.csv"

    file_exists = os.path.isfile(log_file)

    with open(log_file, mode="a", newline="") as file:
      writer = csv.writer(file)

      if not file_exists:
        writer.writerow(["Name", "Age", "BMI", "Risk Level", "Probability"])

      writer.writerow([
        name,
        age,
        round(bmi, 2),
        prediction["risk_level"],
        round(prediction["probability"], 2)
    ])

if __name__ == "__main__":
    main()
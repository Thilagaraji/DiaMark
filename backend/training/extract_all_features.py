import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd

from fingerprint_processing.preprocessing import preprocess_fingerprint
from fingerprint_processing.extractor import extract_features
# FOLDERS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FVC_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../dataset/fingerprints"))
STUDENT_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../dataset/students_raw"))
OUTPUT_FILE = os.path.abspath(os.path.join(BASE_DIR, "../../trained_features/combined_features.csv"))
data = []

def process_folder(folder_path, label):
    for root, dirs, files in os.walk(folder_path):   # 🔥 handles subfolders
        for file in files:
            if file.endswith((".png", ".tif", ".jpg")):
                path = os.path.join(root, file)

                try:
                    img = preprocess_fingerprint(path)
                    features = extract_features(img)

                    row = [
                        features["ridge_density"],
                        features["ridge_thickness"],
                        features["ridge_ratio"],
                        features["minutiae_points"],
                        label
                    ]

                    data.append(row)

                    print("Processed:", path)

                except Exception as e:
                    print("Error:", path, e)
# 🔥 PROCESS DATA

print("Processing FVC2002...")
process_folder(FVC_PATH, 0)   # non-diabetic

print("Processing Students Diabetic...")
process_folder(os.path.join(STUDENT_PATH, "diabetic"), 1)

print("Processing Students Non-Diabetic...")
process_folder(os.path.join(STUDENT_PATH, "non_diabetic"), 0)
# SAVE
df = pd.DataFrame(data, columns=[
    "ridge_density",
    "ridge_thickness",
    "ridge_ratio",
    "minutiae_points",
    "label"
])

df.to_csv(OUTPUT_FILE, index=False)

print("✅ Saved:", OUTPUT_FILE)
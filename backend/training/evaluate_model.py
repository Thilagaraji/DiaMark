import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import joblib

# -------------------------------
# PATH SETUP
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../trained_features/final_dataset.csv"))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "../models/xgb_model.pkl"))

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------
# LOAD DATA
# -------------------------------
print("📂 Loading dataset...")
data = pd.read_csv(DATA_PATH)

if data.empty:
    raise ValueError("❌ Dataset is empty!")

print("✅ Dataset loaded:", data.shape)

# -------------------------------
# FEATURES & LABEL
# -------------------------------
X = data.drop("label", axis=1)
y = data["label"]

# -------------------------------
# NORMALIZATION
# -------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------------------------------
# TRAIN TEST SPLIT
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------
# XGBOOST MODEL (OPTIMIZED)
# -------------------------------
model = XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    eval_metric="logloss"
)

# -------------------------------
# TRAINING
# -------------------------------
print("🚀 Training XGBoost model...")
model.fit(X_train, y_train)

# -------------------------------
# PREDICTION
# -------------------------------
y_pred = model.predict(X_test)

# -------------------------------
# METRICS
# -------------------------------
accuracy = accuracy_score(y_test, y_pred)

print("\n✅ Accuracy:", accuracy)
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

# -------------------------------
# CONFUSION MATRIX
# -------------------------------
cm = confusion_matrix(y_test, y_pred)

plt.figure()
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.colorbar()
plt.xlabel("Predicted")
plt.ylabel("Actual")

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, cm[i][j], ha="center", va="center")

cm_path = os.path.join(OUTPUT_DIR, "confusion_matrix.png")
plt.savefig(cm_path)
plt.close()

print("🖼 Confusion Matrix saved at:", cm_path)

# -------------------------------
# LEARNING CURVE (FIXED ERROR)
# -------------------------------
print("📈 Generating learning curve...")

train_sizes, train_scores, test_scores = learning_curve(
    model,
    X_scaled,
    y,
    cv=5,
    scoring="accuracy",
    train_sizes=np.linspace(0.2, 1.0, 5)  # 🔥 reduced to avoid failure
)

train_mean = np.mean(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)

plt.figure()
plt.plot(train_sizes, train_mean, label="Train Score")
plt.plot(train_sizes, test_mean, label="Test Score")

plt.xlabel("Training Size")
plt.ylabel("Accuracy")
plt.title("Learning Curve")
plt.legend()

lc_path = os.path.join(OUTPUT_DIR, "learning_curve.png")
plt.savefig(lc_path)
plt.close()

print("📊 Learning Curve saved at:", lc_path)

# -------------------------------
# SAVE MODEL + SCALER
# -------------------------------
joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, MODEL_PATH.replace(".pkl", "_scaler.pkl"))

print("💾 Model saved at:", MODEL_PATH)

print("\n🎯 DONE — FINAL MODEL READY")
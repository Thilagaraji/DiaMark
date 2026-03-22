🩺 DiaMark
Diabetes Risk Prediction Using Fingerprint Biometrics

DiaMark is a non-invasive diabetes risk prediction system that uses fingerprint image features (dermatoglyphics) combined with basic health parameters to estimate the likelihood of Type-II Diabetes Mellitus.

The system is implemented as a web-based application (Flask + Frontend UI) that generates a professional PDF medical report, without requiring blood tests.

📌 Key Features
🧬 Biometric-based prediction using fingerprint ridge features
🩸 Completely non-invasive (no blood sample required)
🤖 Machine Learning using XGBoost
🧠 Explainable AI using Fuzzy Logic
🌐 Web-based system (Frontend + Flask API)
📄 Automatic PDF report generation
📊 Model evaluation (Accuracy, Confusion Matrix, Learning Curve)
📝 CSV logging of predictions
🎯 Project Objective

The objective of DiaMark is to develop an early diabetes risk assessment system that is:

Cost-effective
Non-invasive
Easy to use via web interface
Interpretable using explainable AI
Suitable for academic research and screening purposes
🧠 Algorithms Used
1️⃣ XGBoost Classifier (Primary Model)

XGBoost is used to predict diabetes risk based on extracted fingerprint features.

Why XGBoost?

High accuracy on structured data
Handles non-linear relationships
Built-in regularization
Works well on small datasets
2️⃣ Fuzzy Logic System (Explainable Layer)

Fuzzy Logic converts model probability into:

LOW
MEDIUM
HIGH

Why Fuzzy Logic?

Medical risk is not binary
Provides human-readable interpretation
Adds explainability to AI predictions
📥 Input Parameters
🖐️ Fingerprint Features (Extracted Automatically)
Ridge Density
Ridge Thickness
Ridge Ratio
Minutiae Points
👤 User Inputs (Frontend Form)
Age
Height & Weight → BMI
Gender
Family History (Yes / No)
Fingerprint Image Upload
🏗️ System Architecture (Workflow)
User (Frontend Form)
        ↓
Fingerprint Image Upload
        ↓
Image Preprocessing (OpenCV)
        ↓
Feature Extraction
        ↓
XGBoost Model Prediction
        ↓
Probability Output
        ↓
Fuzzy Logic Conversion
        ↓
Risk Level (LOW / MEDIUM / HIGH)
        ↓
PDF Report Generation
        ↓
Result Display (Frontend UI)
🧩 Module Description
Module 1 – User Input (Frontend)
Collects user details and fingerprint image
Sends data to backend API
Module 2 – Image Processing
Preprocess fingerprint image
Enhance quality and remove noise
Module 3 – Feature Extraction

Extracts:

Ridge Density
Ridge Thickness
Ridge Ratio
Minutiae Points
Module 4 – Machine Learning Prediction
XGBoost predicts probability of diabetes risk
Module 5 – Fuzzy Logic Interpretation
Converts probability → risk level
Adds interpretability
Module 6 – Report Generation
Generates PDF report with:
Patient details
Risk level
Model confidence
Explanation
📊 Model Performance
Accuracy: ~97%
Strength: High overall performance
Limitation: Lower recall for diabetic class (due to dataset imbalance)
📂 Dataset Used

This project uses a combined dataset:

T2DM Dataset
Clinical diabetes data
Adds medical relevance
FVC2002 Fingerprint Dataset
Standard biometric dataset
Used as non-diabetic samples
Student Fingerprint Dataset
Real-world collected data
Adds novelty
💻 Technologies Used
Python
Flask (Backend API)
HTML, CSS, JavaScript (Frontend)
XGBoost
Scikit-learn
OpenCV
NumPy & Pandas
Matplotlib
ReportLab (PDF generation)
▶️ How to Run
1. Clone Repository
git clone https://github.com/ThilagarajiDiaMark.git
cd DiaMark
2. Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Run Backend
cd backend
python app.py
5. Open Frontend
Open your frontend (HTML/React) in browser
Connect to:
http://127.0.0.1:5000
📄 Output
Diabetes Risk Level → LOW / MEDIUM / HIGH
Model Probability
Model Confidence
Fingerprint Pattern
Downloadable PDF Report
⚠️ Disclaimer

This system is intended for academic and research purposes only.
It is not a medical diagnostic tool. Always consult a healthcare professional.

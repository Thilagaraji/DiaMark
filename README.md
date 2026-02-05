🩺 DiaMark
Diabetes Risk Prediction Using Fingerprint Biometrics

DiaMark is a non-invasive diabetes risk prediction system that uses fingerprint biometric features combined with basic health parameters to estimate the likelihood of Type-II diabetes.

The system is implemented as a console-based Python application that produces a professional PDF medical report along with voice-assisted explanations, without requiring blood tests, web apps, or mobile interfaces.

📌 Key Features

🧬 Biometric-based prediction using fingerprint ridge features

🩸 Completely non-invasive (no blood sample required)

🤖 Modern machine learning using XGBoost

🧠 Explainable AI through Fuzzy Logic reasoning

📄 Automatic PDF report generation

🔊 Voice-assisted explanation of prediction results

💻 Runs in console/terminal (no web dependency)

🔌 Supports low-cost optical fingerprint scanners

🎯 Project Objective

The objective of DiaMark is to design an early diabetes risk assessment system that is:

Cost-effective

Easy to deploy in low-resource environments

Interpretable and explainable for medical understanding

Suitable for academic research and healthcare screening

🧠 Algorithms Used
1️⃣ XGBoost Classifier (Primary Model)

XGBoost (Extreme Gradient Boosting) is used to classify diabetes risk into:

LOW

MEDIUM

HIGH

Why XGBoost?

High accuracy on structured biomedical data

Handles non-linear relationships effectively

Built-in regularization reduces overfitting

Often outperforms Random Forest and Decision Trees

2️⃣ Fuzzy Logic System (Explainable AI Layer)

Fuzzy Logic converts model predictions into human-readable medical explanations.

Why Fuzzy Logic?

Medical risk is uncertain and gradual, not binary

Translates numbers into linguistic terms (Low / Medium / High)

Generates rule-based explanations & lifestyle advice

Improves transparency, trust, and interpretability

📥 Input Parameters
Fingerprint Features

Ridge Count

Ridge Density

Ridge Thickness

Minutiae Count

Health Parameters

BMI

Family History (Yes / No)

Activity Level (Low / Medium / High)

🏗️ System Architecture (Workflow)
Fingerprint Scanner / Manual Input
            ↓
Feature Preprocessing
            ↓
XGBoost Classifier
            ↓
Diabetes Risk Prediction (LOW / MEDIUM / HIGH)
            ↓
Fuzzy Logic Explanation
            ↓
PDF Report Generation
            ↓
Voice-Assisted Output

🧩 Module Description
Module 1 – Data Input

Collects fingerprint and health features

Accepts numeric and categorical inputs

Module 2 – Feature Preprocessing

Normalization of numeric values

Encoding of categorical variables

Creation of ML feature vector

Module 3 – Machine Learning Prediction

XGBoost predicts diabetes risk level

Module 4 – Explanation Engine

Fuzzy rules generate risk interpretation

Produces diet & lifestyle recommendations

Module 5 – Report & Voice Output

Generates professional PDF medical report

Provides voice explanation of results

🔧 Hardware Requirements

Processor: Intel i3 / AMD Ryzen 3 or higher

RAM: Minimum 4 GB (8 GB recommended)

Storage: 100 GB

Fingerprint Scanner

R307 Optical Fingerprint Sensor

USB-supported

Low power consumption

💻 Software Requirements

Python 3.x

Required Libraries

xgboost

scikit-learn

numpy

pandas

pyttsx3 or gTTS

reportlab or fpdf

Operating System: Windows / Linux

▶️ How to Run the Project
1. Clone the repository
git clone https://github.com/your-username/DiaMark.git

2. Install dependencies
pip install -r requirements.txt

3. Run the application
python main.py


Enter required inputs in the console

View the auto-generated PDF report

Listen to the voice explanation

📄 Output

Diabetes Risk Level → LOW / MEDIUM / HIGH

Generated PDF Report Includes:

Patient input summary

Prediction result

Fuzzy explanation

Lifestyle recommendations

Voice Output

Spoken explanation of diabetes risk

🚀 Future Enhancements

Validation with larger clinical datasets

Support for additional biometric indicators

Model performance visualization dashboard

Optional mobile or web interface integration

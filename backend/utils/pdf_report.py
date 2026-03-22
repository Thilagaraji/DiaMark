from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import time

def generate_report(name, age, bmi, pattern, risk, probability, folder):
    filename = f"report_{int(time.time())}.pdf"
    filepath = os.path.join(folder, filename)

    c = canvas.Canvas(filepath, pagesize=letter)

    # 🏥 TITLE
    c.setFont("Helvetica-Bold", 16)
    c.drawString(140, 750, "DiaMark Diabetes Risk Report")

    # Subtitle
    c.setFont("Helvetica", 10)
    c.drawString(180, 735, "AI-Based Health Assessment System")

    # 👤 PATIENT DETAILS
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 700, "Patient Details")

    c.setFont("Helvetica", 11)
    c.drawString(100, 680, f"Name: {name}")
    c.drawString(100, 660, f"Age: {age}")
    c.drawString(100, 640, f"BMI: {bmi:.2f}")
    c.drawString(100, 620, f"Fingerprint Pattern: {pattern}")  # ✅ FIXED

    # 📊 RESULT
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 590, "Prediction Result")

    c.setFont("Helvetica", 11)
    c.drawString(100, 570, f"Risk Level: {risk}")
   

    # 🧠 INTERPRETATION
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 520, "Interpretation")

    c.setFont("Helvetica", 11)

    if risk == "LOW":
        text = "Low probability of diabetes. Maintain a healthy lifestyle."
    elif risk == "MEDIUM":
        text = "Moderate risk detected. Regular monitoring is advised."
    else:
        text = "High risk detected. Please consult a medical professional."

    c.drawString(100, 500, text)

    # 💡 RECOMMENDATIONS
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 470, "Recommendations")

    c.setFont("Helvetica", 11)
    c.drawString(100, 450, "- Balanced diet")
    c.drawString(100, 435, "- Regular exercise")
    c.drawString(100, 420, "- Monitor blood sugar levels")
    c.drawString(100, 405, "- Consult doctor if needed")

    # ⚠ DISCLAIMER
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 370, "Disclaimer")

    c.setFont("Helvetica", 9)
    c.drawString(100, 350, "This report is AI-generated for academic purposes only.")
    c.drawString(100, 335, "It is not a medical diagnosis.")

    c.save()

    return filename
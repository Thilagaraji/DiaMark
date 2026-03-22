from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import sys
import os

# Add backend folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from voice.voice_reader import speak
from voice.report_ui import open_voice_panel
def generate_report(data):

    REPORT_DIR = "reports"
    os.makedirs(REPORT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(REPORT_DIR, f"report_{timestamp}.pdf")
  
    c = canvas.Canvas(output_file, pagesize=letter)
    _, height = letter
    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(150, y, "DiaMark Diabetes Risk Assessment Report")

    y -= 40

    # Date
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    y -= 40

    # Patient Info
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Patient Information")

    y -= 20
    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Name: {data['name']}")
    y -= 20
    c.drawString(50, y, f"Age: {data['age']}")
    y -= 20
    c.drawString(50, y, f"Gender: {data['gender']}")

    y -= 40

    # Health Info
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Health Analysis")

    y -= 20
    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"BMI: {data['bmi']}")
    y -= 20
    c.drawString(50, y, f"BMI Category: {data['bmi_category']}")

    y -= 40

    # Fingerprint
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Fingerprint Analysis")

    y -= 20
    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Fingerprint Pattern: {data['pattern']}")

    y -= 40

    # Prediction
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Prediction Result")

    y -= 20
    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Risk Level: {data['risk_level']}")
    y -= 20
    c.drawString(50, y, f"Probability: {data['probability']}")

    y -= 40

    # Explanation
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Clinical Explanation")

    y -= 20
    c.setFont("Helvetica", 11)

    for text in data["explanation"]:
        c.drawString(60, y, f"• {text}")
        y -= 20

    y -= 20

    # Recommendations
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Recommendations")

    y -= 20
    c.setFont("Helvetica", 11)

    for text in data["recommendations"]:
        c.drawString(60, y, f"• {text}")
        y -= 20

    c.save()

    print("Report generated:", output_file)

    # Open PDF automatically
    os.startfile(output_file)

    # Voice explanation
    voice_text = f"""
    Hello {data['name']}.
    Your diabetes risk level is {data['risk_level']}.
    Your body mass index is {data['bmi']}.
    The detected fingerprint pattern is {data['pattern']}.
    Please review the generated medical report for detailed analysis.
    """

    speak(voice_text)

    # Open voice panel
    open_voice_panel(data)
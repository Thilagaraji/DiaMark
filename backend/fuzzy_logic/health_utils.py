def calculate_bmi(height_cm, weight_kg):
    """
    Calculate BMI using height and weight
    """

    height_m = height_cm / 100

    bmi = weight_kg / (height_m ** 2)

    return round(bmi, 2)


def bmi_category(bmi):
    """
    Classify BMI level
    """

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"
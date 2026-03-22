def calculate_bmi(height, weight):

    if height <= 0 or weight <= 0:
        raise ValueError("Height and Weight must be positive numbers.")

    # convert cm to meters automatically
    if height > 10:
        height = height / 100

    bmi = weight / (height ** 2)

    return round(bmi, 2)
def bmi_category(bmi):
    """
    Return BMI category based on WHO classification
    """
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"
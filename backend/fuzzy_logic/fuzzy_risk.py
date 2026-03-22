def explain_risk(probability, bmi, family_history):
    """
    Generate detailed medical-style explanation for diabetes risk
    based on fuzzy reasoning combining BMI, family history and
    machine learning prediction probability.
    """

    # Determine risk level from ML probability
    if probability < 0.33:
        risk = "LOW"
    elif probability < 0.66:
        risk = "MEDIUM"
    else:
        risk = "HIGH"


    explanation = []
    recommendations = []
    clinical_notes = []


    # -------------------------------------------------
    # BMI ANALYSIS
    # -------------------------------------------------

    if bmi >= 30:

        explanation.append(
            "The calculated Body Mass Index (BMI) falls within the obese range. "
            "Obesity is widely recognized as one of the most significant risk "
            "factors associated with the development of Type II Diabetes Mellitus. "
            "Excess adipose tissue contributes to metabolic imbalance and "
            "increases insulin resistance, which reduces the body's ability "
            "to effectively regulate blood glucose levels."
        )

        clinical_notes.append(
            "Clinical studies indicate that individuals with BMI above 30 "
            "have a significantly higher likelihood of developing insulin "
            "resistance and impaired glucose tolerance."
        )

        recommendations.append(
            "Weight management through structured dietary planning and "
            "regular physical activity is strongly recommended to reduce "
            "metabolic risk."
        )

    elif bmi >= 25:

        explanation.append(
            "The calculated BMI indicates that the individual is in the "
            "overweight category. Epidemiological research suggests that "
            "excess body weight can increase the probability of developing "
            "metabolic disorders including Type II Diabetes."
        )

        clinical_notes.append(
            "Overweight individuals may gradually develop insulin resistance "
            "due to increased fatty tissue which interferes with glucose "
            "metabolism."
        )

        recommendations.append(
            "Adopting a balanced nutritional diet and maintaining regular "
            "physical activity can significantly reduce diabetes risk."
        )

    else:

        explanation.append(
            "The calculated BMI falls within the normal healthy range. "
            "This indicates that body weight is not currently a major "
            "contributing risk factor for diabetes development."
        )

        clinical_notes.append(
            "Maintaining a normal BMI is considered protective against "
            "many metabolic disorders including diabetes."
        )

        recommendations.append(
            "Continue maintaining a balanced diet and healthy lifestyle."
        )


    # -------------------------------------------------
    # FAMILY HISTORY ANALYSIS
    # -------------------------------------------------

    if family_history:

        explanation.append(
            "The presence of a positive family history of diabetes suggests "
            "a potential genetic predisposition. Individuals with diabetic "
            "parents or close relatives may inherit metabolic traits that "
            "increase susceptibility to impaired glucose regulation."
        )

        clinical_notes.append(
            "Genetic predisposition is considered an important non-modifiable "
            "risk factor in diabetes risk assessment."
        )

        recommendations.append(
            "Periodic blood glucose monitoring and preventive lifestyle "
            "management are recommended due to hereditary risk."
        )

    else:

        explanation.append(
            "No direct family history of diabetes was reported. This reduces "
            "the likelihood of inherited metabolic susceptibility."
        )

        clinical_notes.append(
            "Absence of hereditary risk does not completely eliminate the "
            "possibility of diabetes development but indicates a relatively "
            "lower genetic risk."
        )


    # -------------------------------------------------
    # MACHINE LEARNING MODEL INTERPRETATION
    # -------------------------------------------------

    if risk == "HIGH":

        explanation.append(
            "The machine learning prediction model identified a high "
            "probability of diabetes risk based on dermatoglyphic "
            "fingerprint patterns combined with the provided health "
            "parameters. Dermatoglyphic analysis has been investigated "
            "in biomedical research as a potential non-invasive marker "
            "for certain genetic and metabolic disorders."
        )

        clinical_notes.append(
            "Fingerprint ridge patterns develop during fetal growth and "
            "remain unchanged throughout life. Some research studies have "
            "reported correlations between dermatoglyphic variations and "
            "metabolic diseases including diabetes."
        )

        recommendations.append(
            "Immediate medical consultation and laboratory screening such "
            "as fasting blood glucose or HbA1c testing are strongly advised."
        )

    elif risk == "MEDIUM":

        explanation.append(
            "The machine learning model indicates a moderate probability "
            "of diabetes risk. While the current indicators do not confirm "
            "the presence of diabetes, certain patterns and health factors "
            "suggest that preventive monitoring may be beneficial."
        )

        clinical_notes.append(
            "Moderate risk levels indicate the presence of some predictive "
            "markers but not strong enough evidence for high-risk classification."
        )

        recommendations.append(
            "Preventive lifestyle modifications including regular physical "
            "exercise and balanced nutrition are recommended."
        )

    else:

        explanation.append(
            "The machine learning analysis indicates a low probability of "
            "diabetes risk at this time. The evaluated biometric and health "
            "parameters do not strongly correlate with patterns commonly "
            "observed in high-risk groups."
        )

        clinical_notes.append(
            "Low risk classification indicates minimal correlation with "
            "known predictive features associated with diabetes."
        )

        recommendations.append(
            "Routine health check-ups and maintaining healthy lifestyle "
            "habits are recommended for long-term metabolic health."
        )


    # -------------------------------------------------
    # FINAL RESULT STRUCTURE
    # -------------------------------------------------

    return {
        "risk_level": risk,
        "explanation": explanation,
        "clinical_notes": clinical_notes,
        "recommendations": recommendations
    }
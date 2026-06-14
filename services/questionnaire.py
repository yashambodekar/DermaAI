def analyze_questionnaire(data):

    score = 0

    recommendations = []

    if data["sleep_hours"] < 6:
        score += 2
        recommendations.append(
            "Increase sleep duration."
        )

    if data["water_intake"].lower() == "low":
        score += 2
        recommendations.append(
            "Increase daily water intake."
        )

    if data["sun_exposure"].lower() == "high":
        score += 2
        recommendations.append(
            "Reduce sun exposure and use sunscreen."
        )

    if data["stress_level"].lower() == "high":
        score += 2
        recommendations.append(
            "Manage stress through exercise and relaxation."
        )

    if score <= 3:
        risk_level = "Low"
    elif score <= 6:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "recommendations": recommendations
    }
import os
import json
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_skin_report(
    cnn_result,
    questionnaire_result,
    user_data
):

    prompt = f"""
You are an expert AI skincare assistant.

A CNN skin disease detection model has already analyzed the skin image.

CNN Prediction:
{cnn_result}

Questionnaire Analysis:
{questionnaire_result}

User Information:
Age: {user_data['age']}
Skin Type: {user_data['skin_type']}
Sleep Hours: {user_data['sleep_hours']}
Water Intake: {user_data['water_intake']}
Sun Exposure: {user_data['sun_exposure']}
Stress Level: {user_data['stress_level']}

IMPORTANT:

- Treat the CNN prediction as the primary skin condition prediction.
- Use questionnaire data to personalize recommendations.
- This is NOT a medical diagnosis.
- Clearly mention that results are AI-generated.
- Do NOT prescribe medication.
- Give safe and practical skincare guidance.
- Recommend skincare product categories, not specific prescription drugs.
- Confidence should be based on the CNN confidence score.

Return ONLY valid JSON.

{{
    "skin_condition":"",
    "severity":"",
    "confidence":"",
    "concerns":[],
    "condition_overview":"",
    "possible_causes":[],
    "morning_routine":[],
    "night_routine":[],
    "foods_to_eat":[],
    "foods_to_avoid":[],
    "recommended_products":[],
    "lifestyle_recommendations":[],
    "consult_dermatologist_when":[],
    "disclaimer":""
}}
"""

    response = model.generate_content(
        prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "")
        text = text.replace("```", "").strip()

    return json.loads(text)
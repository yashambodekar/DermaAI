import os
import json
import google.generativeai as genai

from PIL import Image
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def analyze_skin_and_generate_report(
    image_path,
    questionnaire_result,
    user_data
):

    image = Image.open(image_path)

    prompt = f"""
You are an AI skincare assistant.

Analyze the uploaded facial image and the questionnaire data.

IMPORTANT:
- This is not a medical diagnosis.
- Mention that results are AI-generated.
- Avoid prescribing medication.
- Give practical skincare guidance.

Questionnaire Result:
{questionnaire_result}

User Details:
Age: {user_data['age']}
Skin Type: {user_data['skin_type']}
Sleep Hours: {user_data['sleep_hours']}
Water Intake: {user_data['water_intake']}
Sun Exposure: {user_data['sun_exposure']}
Stress Level: {user_data['stress_level']}

Return ONLY VALID JSON:

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
    "consult_dermatologist_when":[]
}}
"""

    response = model.generate_content(
        [prompt, image]
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "")
        text = text.replace("```", "").strip()

    return json.loads(text)
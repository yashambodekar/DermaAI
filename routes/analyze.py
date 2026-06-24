import os
import uuid

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form

from services.questionnaire import (
    analyze_questionnaire
)

from services.gemini_service import (
    generate_skin_report
)

from services.predictor import (
    predict_skin_disease
)

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/analyze")
async def analyze_skin(

    image: UploadFile = File(...),

    age: int = Form(...),

    skin_type: str = Form(...),

    sleep_hours: int = Form(...),

    water_intake: str = Form(...),

    sun_exposure: str = Form(...),

    stress_level: str = Form(...)
):

    file_extension = image.filename.split(".")[-1]

    filename = (
        f"{uuid.uuid4()}.{file_extension}"
    )

    image_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(image_path, "wb") as buffer:
        buffer.write(
            await image.read()
        )

    user_data = {
        "age": age,
        "skin_type": skin_type,
        "sleep_hours": sleep_hours,
        "water_intake": water_intake,
        "sun_exposure": sun_exposure,
        "stress_level": stress_level
    }

    questionnaire_result = (
        analyze_questionnaire(
            user_data
        )
    )

    # CNN Prediction from Hugging Face
    cnn_result = (
        predict_skin_disease(
            image_path
        )
    )
    
    try:
     cnn_result = predict_skin_disease(image_path)
    except Exception:
     cnn_result = {
        "Disease": "Unknown",
        "Confidence (%)": 0
    }

    # Gemini Report Generation
    report = (
        generate_skin_report(
            cnn_result,
            questionnaire_result,
            user_data
        )
    )

    if os.path.exists(image_path):
        os.remove(image_path)

    return {
        "cnn_prediction": cnn_result,
        "questionnaire": questionnaire_result,
        "analysis": report
    }
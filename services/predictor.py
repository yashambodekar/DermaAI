import json
import numpy as np
import tensorflow as tf

from PIL import Image


# ==========================
# Load Model Once
# ==========================

model = tf.keras.models.load_model(
    "model/best_skin_model.keras"
)

# ==========================
# Load Classes
# ==========================

with open("model/classes.json", "r") as f:
    classes = json.load(f)

# ==========================
# Load Friendly Names
# ==========================

with open("model/class_mapping.json", "r") as f:
    class_mapping = json.load(f)


# ==========================
# Prediction Function
# ==========================

def predict_skin_disease(image_path):

    # Load image
    image = Image.open(image_path).convert("RGB")

    image = image.resize((224, 224))

    image_array = np.array(image)

    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(
        image_array
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # Predict
    prediction = model.predict(
        image_array,
        verbose=0
    )

    predicted_index = np.argmax(prediction)

    confidence = float(
        np.max(prediction) * 100
    )

    if confidence >= 80:
     severity = "High Confidence"
    elif confidence >= 60:
     severity = "Moderate Confidence"
    else:
     severity = "Low Confidence"

    original_class = classes[predicted_index]

    display_class = class_mapping.get(
        original_class,
        original_class
    )

    return {
        "condition": display_class,
        "confidence": round(confidence, 2),
        "prediction_quality": severity
    }
import os

from gradio_client import Client, handle_file

client = Client("Ambodekar/skincnn")


def predict_skin_disease(image_path):
    image_path = os.path.normpath(image_path)
    if not os.path.isabs(image_path):
        image_path = os.path.abspath(image_path)

    result = client.predict(
        image=handle_file(image_path),
        api_name="/predict"
    )

    return result
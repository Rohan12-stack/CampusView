# src/model_utils.py
import base64
import requests
from io import BytesIO
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from src.config import CFG

# -----------------------
# 1. Local Caption Model
# -----------------------
def generate_caption_local(pil_image):
    """
    Generates a short caption for the given image using a local BLIP model.
    """
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    inputs = processor(pil_image, return_tensors="pt")
    out = model.generate(**inputs, max_length=30)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption


# -----------------------
# 2. Groq API Connector
# -----------------------
def call_groq_api(prompt, meta=None):
    """
    Calls the Groq API with a structured prompt.
    Expects CFG.GROQ_API_KEY and CFG.GROQ_API_URL to be set.
    Returns a short conversational answer.
    """
    headers = {
        "Authorization": f"Bearer {CFG.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    # ✅ Ensure model name matches your Groq model
    model_name = "llama-3.1-70b-versatile"  # or your preferred Groq model

    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": (
                "You are CampusView, a friendly AI assistant that answers questions "
                "about college facilities based on images and text descriptions. "
                "Always reply in 1–2 short, human-like sentences."
            )},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.6,
        "max_tokens": 150
    }

    try:
        response = requests.post(CFG.GROQ_API_URL, headers=headers, json=data, timeout=20)

        if response.status_code != 200:
            raise Exception(f"Groq API Error: {response.status_code} — {response.text}")

        result = response.json()
        # Extract model output safely
        message = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if not message:
            message = "I'm not sure, but it seems related to a college environment."

        return message

    except Exception as e:
        print(f"[Groq API Error] {e}")
        return "Unable to get response from Groq API. Please try again."


# -----------------------
# 3. Optional Helper: Convert image to bytes (for OCR or upload)
# -----------------------
def pil_to_bytes(pil_image):
    """
    Converts PIL image to byte array (useful for Groq or OCR).
    """
    buf = BytesIO()
    pil_image.save(buf, format="JPEG")
    byte_data = buf.getvalue()
    return byte_data

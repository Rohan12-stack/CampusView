# src/preprocess.py
from PIL import Image
import pytesseract
import io

def pil_to_bytes(image):
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    return buf.getvalue()

def run_ocr(pil_image):
    """
    Return OCR text found in image. Requires Tesseract installed on system.
    On Windows install Tesseract and ensure PATH includes tesseract.exe or set pytesseract.pytesseract.tesseract_cmd.
    """
    try:
        text = pytesseract.image_to_string(pil_image)
        return text.strip()
    except Exception as e:
        return ""

from src.model_utils import generate_caption_local
from src.preprocess import run_ocr
from src.config import CFG
import json
import os

# -------------------------------
# Load facility data
# -------------------------------
FACILITY_DATA = {}
try:
    with open("data/annotations.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            if "facility" in item:
                FACILITY_DATA[item["facility"].lower()] = item
except Exception as e:
    print("Warning: Could not load annotations.jsonl:", e)

# -------------------------------
# Facility detection logic
# -------------------------------
def detect_facility(caption, ocr_text="", image_path=None):
    """Detect which facility the image likely represents"""
    text = (caption + " " + (ocr_text or "")).lower()

    # Use filename as fallback
    if image_path:
        filename = os.path.basename(image_path).lower()
        text += " " + filename

    if "library" in text:
        return "library"
    elif "lab" in text or "computer" in text:
        return "computer lab"
    elif "gate" in text or "entrance" in text or "exit" in text:
        return "back gate"
    return None

# -------------------------------
# Response logic
# -------------------------------
def answer_from_caption_and_question(caption, question, ocr_text=None, image_path=None):
    q_lower = question.lower()
    facility = detect_facility(caption, ocr_text, image_path)

    if facility not in FACILITY_DATA:
        return "This looks like a part of the college campus."

    data = FACILITY_DATA[facility]
    timings = data.get("timings", "")
    desc = data.get("description", "")
    location = data.get("location", "")

    # 1️⃣ What place is this
    if any(x in q_lower for x in ["what is this", "what place", "where am i", "what can you see"]):
        if facility == "computer lab":
            return (
                "This is our campus Computer Lab. The lab features high-performance systems with development tools "
                "and internet access for student projects. It is used for practical sessions, programming labs, and project work."
            )
        elif facility == "library":
            return (
                "This is our campus Library. The library provides books, journals, and a calm study space for students. "
                "Students use this place for reading, research, and accessing digital resources."
            )
        elif facility == "back gate":
            return (
                "This is our campus Back Gate. It serves as an additional entrance and exit, monitored by security personnel "
                "and CCTV cameras for safety."
            )

    # 2️⃣ Timings / Opening hours
    elif any(x in q_lower for x in ["timing", "when", "open", "close", "enter"]):
        if facility == "computer lab":
            return "The Computer Lab is open Monday to Saturday 9 AM to 5 PM, Sunday labs are closed."
        elif facility == "library":
            return "The Library is open Monday to Saturday 10 AM to 5 PM, Sunday library is closed."
        elif facility == "back gate":
            return "The Back Gate is open Monday to Friday 9 AM to 5 PM, weekends the gate will be closed."

    # 3️⃣ Facilities / What's inside
    elif any(x in q_lower for x in ["facility", "facilities", "what are there", "what is there", "available", "sections"]):
        if facility == "computer lab":
            return (
                "The Computer Lab has 32 HP desktop systems with Core i7 processors, 16GB RAM, and 1Gbps LAN connectivity. "
                "It includes Programming and Network Lab sections for hands-on student work."
            )
        elif facility == "library":
            return (
                "The Library has multiple sections of books including Reading Hall, Reference Section, and Digital Library. "
                "Students are provided chairs and tables with plug sockets to charge devices, and high-speed Wi-Fi is available for internet access."
            )
        elif facility == "back gate":
            return (
                "The Back Gate area has two security guards, CCTV cameras for 24-hour surveillance, "
                "and students must wear ID cards to enter."
            )

    # 4️⃣ Location / Where
    elif any(x in q_lower for x in ["where", "location", "located"]):
        return f"The {facility.capitalize()} is located at {location}."

    # 5️⃣ Default fallback
    return f"This is our campus {facility.capitalize()}. {desc}"

# -------------------------------
# Inference pipeline
# -------------------------------
def infer(pil_image, question, image_path=None):
    """Main inference pipeline"""
    try:
        caption = generate_caption_local(pil_image)
    except Exception as e:
        caption = ""
        print("Captioning error:", e)

    ocr_text = run_ocr(pil_image)
    answer = answer_from_caption_and_question(caption, question, ocr_text, image_path)

    return {"answer": answer, "caption": caption, "ocr_text": ocr_text, "objects": []}

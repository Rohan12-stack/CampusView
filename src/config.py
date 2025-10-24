# src/config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    # ----------------------------
    # Groq configuration
    # ----------------------------
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_API_URL = os.getenv(
        "GROQ_API_URL",
        "https://api.groq.com/openai/v1/chat/completions"  # ✅ default API endpoint
    )

    # ----------------------------
    # Model backend and device
    # ----------------------------
    MODEL_BACKEND = os.getenv("MODEL_BACKEND", "groq")  # Default to Groq now
    DEVICE = os.getenv("DEVICE", "cpu")

    # ----------------------------
    # Safety check
    # ----------------------------
    @staticmethod
    def check():
        if Config.MODEL_BACKEND == "groq" and not Config.GROQ_API_KEY:
            raise ValueError("❌ Missing GROQ_API_KEY in environment variables. Please add it to your .env file.")

CFG = Config()

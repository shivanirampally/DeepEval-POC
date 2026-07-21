import os

from dotenv import load_dotenv
from deepeval.models import GeminiModel

from config.app_config import GEMINI_MODEL

from utils.logger import (
    info,
    success,
)

load_dotenv()


def load_gemini_model():

    info("Initializing Gemini Judge...")

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in .env"
        )

    model = GeminiModel(
        model=GEMINI_MODEL,
        api_key=api_key,
    )

    success(f"Gemini Judge Ready ({GEMINI_MODEL})")

    return model
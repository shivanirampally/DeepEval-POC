import os
from dotenv import load_dotenv
from deepeval.models import GeminiModel

load_dotenv()

def load_model():
    return GeminiModel(
        model="gemini-pro-latest",
        api_key=os.getenv("GOOGLE_API_KEY")
    )
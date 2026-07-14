from google import genai

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


class GeminiProvider:
    """
    Handles communication with Gemini API.
    """

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate_response(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text
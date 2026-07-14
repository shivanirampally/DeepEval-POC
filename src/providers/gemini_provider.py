from google import genai

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


class GeminiProvider:
    """
    Handles communication with the Gemini API.
    """

    def __init__(self):

        if not GEMINI_API_KEY:
            raise ValueError(
                "Gemini API Key is missing."
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate_response(
        self,
        prompt: str
    ) -> str:
        """
        Sends the prompt to Gemini and
        returns the generated response.
        """

        if not prompt or not str(prompt).strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=str(prompt).strip()
        )

        if not response or not response.text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        return response.text.strip()
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

        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_response(self, prompt: str) -> str:
        """
        Sends a prompt to Gemini and returns the response.
        """

        try:

            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

            return response.text

        except Exception as error:

            print(f"Gemini Error: {error}")

            return None
import requests

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    TEMPERATURE,
)


class GeminiService:
    """
    Service responsible for communicating
    with the Google Gemini API.

    The service accepts a prompt and model,
    and returns the raw generated response.
    """

    BASE_URL = (
        "https://generativelanguage.googleapis.com/v1beta/models"
    )

    @staticmethod
    def generate_response(
        *,
        prompt: str,
        model: str = GEMINI_MODEL,
    ) -> str:

        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        # Prevent duplicate "models/" prefix
        model = model.removeprefix("models/")

        url = (
            f"{GeminiService.BASE_URL}/"
            f"{model}:generateContent"
        )

        params = {
            "key": GEMINI_API_KEY,
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt,
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": TEMPERATURE,
                "responseMimeType": "application/json",
            },
        }

        response = requests.post(
            url,
            params=params,
            json=payload,
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        try:
            return (
                data["candidates"][0]
                ["content"]
                ["parts"][0]
                ["text"]
            )

        except (KeyError, IndexError, TypeError) as exception:

            raise ValueError(
                "Unexpected Gemini API response format."
            ) from exception
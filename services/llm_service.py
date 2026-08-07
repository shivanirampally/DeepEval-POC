import requests

from config.settings import (
    OLLAMA_URL,
    OLLAMA_TIMEOUT,
    TEMPERATURE,
)


class LLMService:
    """
    Central service responsible for communicating
    with all LLM providers.

    Currently supports:
        • QA Boat (Qwen)
        • Phi3
        • Qwen
        • Future Ollama models
    """

    @staticmethod
    def generate_response(
        *,
        prompt: str,
        model: str,
    ) -> str:

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": TEMPERATURE,
            },
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=OLLAMA_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()["response"]
import requests

from config.settings import (
    OLLAMA_TIMEOUT,
    TEMPERATURE,
)


class LLMService:
    """
    Central service for Ollama-based generators.

    Supports different Ollama endpoints through
    the base_url parameter.

    Examples:
        Qwen3 -> remote Ollama server
        Phi3  -> local Ollama server
    """

    @staticmethod
    def generate_response(
        *,
        prompt: str,
        model: str,
        base_url: str,
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
            base_url,
            json=payload,
            timeout=OLLAMA_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]
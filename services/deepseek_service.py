import requests

from config.settings import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
    DEEPSEEK_TIMEOUT,
    TEMPERATURE,
)


class DeepSeekService:

    @staticmethod
    def generate_response(
        *,
        prompt: str,
        model: str = DEEPSEEK_MODEL,
    ) -> str:

        if not DEEPSEEK_API_KEY:
            raise ValueError(
                "DEEPSEEK_API_KEY is not configured."
            )

        response = requests.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                "Authorization": (
                    f"Bearer {DEEPSEEK_API_KEY}"
                ),
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "temperature": TEMPERATURE,
                "stream": False,
                "response_format": {
                    "type": "json_object"
                },
            },
            timeout=DEEPSEEK_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]
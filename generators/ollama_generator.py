import ollama

from config.app_config import (
    OLLAMA_MODEL,
    TEMPERATURE,
)


def generate_response(prompt):

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        options={
            "temperature": TEMPERATURE,
        },
    )

    return response["message"]["content"]
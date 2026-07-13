import ollama
from deepeval.models import OllamaModel


def load_model():
    return OllamaModel(model="phi3")


def generate_response(prompt):
    response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
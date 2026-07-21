from datetime import datetime

from config.app_config import (
    DATASET_PATH,
    GEMINI_MODEL,
    MAX_TESTS,
    OLLAMA_MODEL,
    TEMPERATURE,
)


def print_banner():

    line = "=" * 78

    print(f"\n{line}")
    print("          AI HALLUCINATION EVALUATION FRAMEWORK")
    print(line)

    print(
        f"\nExecution Started : "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print("\nConfiguration")
    print("-" * 78)
    print(f"Dataset        : {DATASET_PATH}")
    print(f"Ollama Model   : {OLLAMA_MODEL}")
    print(f"Gemini Judge   : {GEMINI_MODEL}")
    print(f"Temperature    : {TEMPERATURE}")
    print(f"Max Test Cases : {MAX_TESTS}")
    print("-" * 78)
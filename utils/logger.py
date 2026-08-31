from datetime import datetime


def _timestamp():
    return datetime.now().strftime("%H:%M:%S")


def header(title):
    line = "=" * 70
    print(f"\n{line}")
    print(title)
    print(line)


def info(message):
    print(f"[{_timestamp()}] {message}")


def success(message):
    print(f"[{_timestamp()}] ✓ {message}")


def failed(message):
    if "RESOURCE_EXHAUSTED" in message:
        message = "Gemini API quota exhausted."

    print(f"[{_timestamp()}] ✗ {message}")


def summary(
    category,
    hallucination,
    correctness,
    relevancy,
    severity,
    severity_score,
):
    print("-" * 70)
    print(f"Category             : {category}")
    print(f"Hallucination Score  : {hallucination}")
    print(f"Correctness Score    : {correctness}")
    print(f"Relevancy Score      : {relevancy}")
    print(f"Severity             : {severity}")
    print(f"Severity Score       : {severity_score}")
    print("-" * 70)
from datetime import datetime


def _timestamp():
    """Return current time in HH:MM:SS format."""
    return datetime.now().strftime("%H:%M:%S")


def blank():
    """Print a blank line."""
    print()


def separator():
    """Print a separator line."""
    print("-" * 70)


def header(title):
    """Print a section header."""
    line = "=" * 70
    print(f"\n{line}")
    print(title)
    print(line)


def info(message):
    """Print an informational message."""
    print(f"[{_timestamp()}] {message}")


def success(message):
    """Print a success message."""
    print(f"[{_timestamp()}] ✓ {message}")


def warning(message):
    """Print a warning message."""
    print(f"[{_timestamp()}] ⚠ {message}")


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
    """Print evaluation summary."""

    separator()

    print(f"Category             : {category}")
    print(f"Hallucination Score  : {hallucination}")
    print(f"Correctness Score    : {correctness}")
    print(f"Relevancy Score      : {relevancy}")
    print(f"Severity             : {severity}")
    print(f"Severity Score       : {severity_score}")

    separator()
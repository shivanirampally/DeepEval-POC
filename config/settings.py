# -----------------------------
# Input / Output
# -----------------------------
INPUT_REQUIREMENT_FILE = "dataset/inputData/requirements.xlsx"
OUTPUT_FOLDER = "dataset/outputData"

# -----------------------------
# Ollama (QA Boat)
# -----------------------------
OLLAMA_URL = "http://192.168.1.81:11434/api/generate"

OLLAMA_TIMEOUT = 300
TEMPERATURE = 0

# -----------------------------
# Gemini
# -----------------------------
GEMINI_MODEL = "gemini-2.5-flash"

# API key will come from .env later

# -----------------------------
# Evaluation
# -----------------------------
HALLUCINATION_THRESHOLD = 0.20
FAITHFULNESS_THRESHOLD = 0.90
CORRECTNESS_THRESHOLD = 0.90
COMPLETENESS_THRESHOLD = 0.90

# -----------------------------
# Logging
# -----------------------------
SHOW_CONSOLE_LOGS = True
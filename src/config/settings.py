from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# Project Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_DATASET = (
    BASE_DIR
    / "dataset"
    / "inputData"
    / "hallucination_dataset.xlsx"
)

OUTPUT_REPORT = (
    BASE_DIR
    / "dataset"
    / "outputData"
    / "evaluation_report.xlsx"
)

# ==========================================
# Dataset Configuration
# ==========================================

REQUIRED_DATASET_COLUMNS = [
    "ID",
    "Hallucination_Type",
    "Provider",
    "Model",
    "Metrics",
    "Input",
    "Context",
    "Expected_Output"
]

# ==========================================
# Gemini Configuration
# ==========================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Used by google-genai SDK
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "models/gemini-flash-latest"
)

# Used by DeepEval GeminiModel
DEEPEVAL_GEMINI_MODEL = os.getenv(
    "DEEPEVAL_GEMINI_MODEL",
    GEMINI_MODEL.replace("models/", "")
)

# ==========================================
# Execution Configuration
# ==========================================

MAX_TEST_CASES = int(
    os.getenv("MAX_TEST_CASES", "5")
)

USE_MOCK_PROVIDER = (
    os.getenv("USE_MOCK_PROVIDER", "True")
    .lower() == "true"
)
from pathlib import Path
import os
from dotenv import load_dotenv

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

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

# Dataset
INPUT_DATASET = BASE_DIR / "dataset" / "inputData" / "hallucination_dataset.xlsx"

# Output
OUTPUT_REPORT = BASE_DIR / "dataset" / "outputData" / "evaluation_report.xlsx"

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MAX_TEST_CASES = int(os.getenv("MAX_TEST_CASES", "5"))

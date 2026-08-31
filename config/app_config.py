import os
from dotenv import load_dotenv

load_dotenv()

# Dataset
DATASET_PATH = "datasets/citation_dataset.xlsx"

# Models
OLLAMA_MODEL = "phi3"
GEMINI_MODEL = "gemini-flash-latest"

# API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Execution
MAX_TESTS = 2
TEMPERATURE = 0

# Evaluation
HALLUCINATION_THRESHOLD = 0.2
RELEVANCY_THRESHOLD = 0.5

# Reports
REPORT_FOLDER = "dataset/outputData/reports"
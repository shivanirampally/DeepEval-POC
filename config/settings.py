"""
Application configuration
"""

# ==========================================================
# Workbook
# ==========================================================

INPUT_WORKBOOK = "datasets/Login_test_repository.xlsx"
OUTPUT_FOLDER = "dataset/outputData"

# ==========================================================
# Excel Sheet Names
# ==========================================================

REQUIREMENT_SHEET = "01_Requirements"
GROUNDTRUTH_SHEET = "02_GroundTruth_TestCases"
METADATA_SHEET = "03_GroundTruth_Metadata"
INPUT_VARIATION_SHEET = "04_InputVariations"
USABILITY_SHEET = "05_UsabilityNavigation"
NON_FUNCTIONAL_SHEET = "06_NonFunctional"

# ==========================================================
# Requirement Parser
# ==========================================================

REQUIRED_REQUIREMENT_COLUMNS = [
    "Requirement ID",
    "Requirement Type",
    "Title",
    "Description/Acceptance Criteria",
    "Business Rules",
    "Priority",
]

# ==========================================================
# Ground Truth Parser
# ==========================================================

REQUIRED_GROUNDTRUTH_COLUMNS = [
    "Requirement ID",
    "Ground Truth",
]

# ==========================================================
# Metadata Parser
# ==========================================================

REQUIRED_METADATA_COLUMNS = [
    "Requirement ID",
    "Module",
]

# ==========================================================
# LLM Configuration
# ==========================================================

OLLAMA_URL = "http://192.168.1.81:11434/api/generate"
OLLAMA_TIMEOUT = 300
TEMPERATURE = 0

GEMINI_MODEL = "gemini-2.5-flash"

# Gemini API Key will be loaded from .env

# ==========================================================
# Generation
# ==========================================================

MIN_TEST_CASES = 5
MAX_TEST_CASES = 15

# ==========================================================
# Evaluation
# ==========================================================

HALLUCINATION_THRESHOLD = 0.20
FAITHFULNESS_THRESHOLD = 0.90
CORRECTNESS_THRESHOLD = 0.90
COMPLETENESS_THRESHOLD = 0.90

MAX_TESTCASES_PER_BATCH = 25

# ==========================================================
# Parallel Execution
# ==========================================================

MAX_CONCURRENT_REQUESTS = 3

# ==========================================================
# Retry Policy
# ==========================================================

MAX_RETRIES = 3
REQUEST_TIMEOUT = 300

# ==========================================================
# Logging
# ==========================================================

SHOW_CONSOLE_LOGS = True
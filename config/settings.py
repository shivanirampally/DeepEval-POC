"""
Application Configuration
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
    "RequirementID",
    "RequirementType",
    "Title",
    "Description/AcceptanceCriteria",
    "BusinessRules",
    "Priority",
]

# ==========================================================
# Ground Truth Parser
# ==========================================================
REQUIRED_GROUNDTRUTH_COLUMNS = [
    "RequirementID",
    "GroundTruth",
]

# ==========================================================
# Metadata Parser
# ==========================================================
REQUIRED_METADATA_COLUMNS = [
    "Requirement ID",
    "Module",
]

# ==========================================================
# QA Boat Generator (Office Ollama)
# ==========================================================
OLLAMA_URL = "http://192.168.1.81:11434/api/generate"
OLLAMA_MODEL = "qwen3-coder:30b"
OLLAMA_TIMEOUT = 300
TEMPERATURE = 0

# ==========================================================
# DeepEval Judge (Local Ollama)
# ==========================================================
JUDGE_PROVIDER = "ollama"
JUDGE_URL = "http://192.168.1.81:11434/api/generate"
JUDGE_MODEL = "gpt-oss:20b"
JUDGE_TIMEOUT = 300

# ==========================================================
# Future Generators
# ==========================================================
GEMINI_MODEL = "gemini-2.5-flash"

# ==========================================================
# Test Case Generation
# ==========================================================
MIN_TEST_CASES = 5
MAX_TEST_CASES = 15

# ==========================================================
# Framework Validation
# ==========================================================
MIN_TEST_STEPS = 2
MAX_TEST_STEPS = 20
MIN_DESCRIPTION_LENGTH = 10
MIN_EXPECTED_RESULT_LENGTH = 10
ALLOW_EMPTY_TESTDATA = False
REQUIRE_UNIQUE_TESTCASE_IDS = True
REQUIRE_UNIQUE_DESCRIPTIONS = True
MIN_COVERAGE_PERCENTAGE = 90

# ==========================================================
# DeepEval Thresholds
# ==========================================================
HALLUCINATION_THRESHOLD = 0.20
CORRECTNESS_THRESHOLD = 0.90
FAITHFULNESS_THRESHOLD = 0.90
COMPLETENESS_THRESHOLD = 0.90
RELEVANCY_THRESHOLD = 0.80

# ==========================================================
# Score Weights
# ==========================================================
SCHEMA_WEIGHT = 0.15
TESTCASE_WEIGHT = 0.25
COVERAGE_WEIGHT = 0.30
DEEPEVAL_WEIGHT = 0.30

# ==========================================================
# Evaluation
# ==========================================================
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

# ==========================================================
# Smoke Test
# ==========================================================
MAX_REQUIREMENTS = None
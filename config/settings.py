"""
Application Configuration
"""
##--------RequirmentSheet validations--------
# Workbook
INPUT_WORKBOOK = ("datasets/LoginFunctionality_RequirmentsRepository.xlsx")
OUTPUT_FOLDER = "dataset/outputData"

# Excel Sheet Names
REQUIREMENT_SHEET = "01_Requirements"
USER_STORY_BENCHMARK_SHEET = ("02_UserStory_Benchmark")
AC_BENCHMARK_SHEET = ("03_AC_Benchmark_TestCases")
INPUT_VARIATION_SHEET = ("04_InputVariations")
USABILITY_SHEET = ("05_UsabilityNavigation")
NON_FUNCTIONAL_SHEET = ("06_NonFunctional")
BENCHMARK_METADATA_SHEET = ("07_Benchmark_Metadata")

# Requirement Sheet
REQUIRED_REQUIREMENT_COLUMNS = [
    "Requirement ID",
    "Requirement Type",
    "Title",
    "Description/Acceptance Criteria",
    "Business Rules",
    "Priority",
]

# User Story Benchmark Sheet
REQUIRED_USER_STORY_BENCHMARK_COLUMNS = [
    "Benchmark TC ID",
    "Requirement ID",
    "Scenario",
    "Category",
    "Priority",
    "Precondition",
    "Test Data",
    "Steps",
    "Expected Result",
    "Source",
    "DeepEval Reference",
]

# Acceptance Criteria Benchmark Sheet
REQUIRED_AC_BENCHMARK_COLUMNS = [
    "TC ID",
    "AC Ref",
    "Test Type",
    "Technique",
    "Priority",
    "Description",
    "Precondition",
    "Test Data",
    "Steps",
    "Expected Result",
    "DeepEval Reference",
]

# Input Variations
REQUIRED_INPUT_VARIATION_COLUMNS = [
    "Requirement ID",
    "Field",
    "Variation",
    "Category",
    "Expected Result",
    "DeepEval Reference",
]

# Usability / Navigation
REQUIRED_USABILITY_COLUMNS = [
    "Requirement ID",
    "Scenario",
    "Category",
    "Expected Result",
    "DeepEval Reference",
]

# Non-Functional
REQUIRED_NON_FUNCTIONAL_COLUMNS = [
    "Requirement ID",
    "Category",
    "Scenario",
    "Expected Result",
    "DeepEval Reference",
]

# Benchmark Metadata
REQUIRED_BENCHMARK_METADATA_COLUMNS = [
    "Field",
    "Value",
]

#---------------Generators---------------------------
## QA Boat
OLLAMA_URL = ("http://192.168.1.81:11434/api/generate")
OLLAMA_MODEL = "qwen3-coder:30b"
OLLAMA_TIMEOUT = 300
TEMPERATURE = 0.5

## Gemini
GEMINI_MODEL = "gemini-2.5-flash"


#---------------Evaluators---------------------------
# DeepEval
JUDGE_PROVIDER = "ollama"
JUDGE_URL = ("http://192.168.1.81:11434/api/generate")
JUDGE_MODEL = "gpt-oss:20b"
JUDGE_TIMEOUT = 300


#----------------Test Case Quality---------------------
#Testcase Quality & Accountability
MIN_TEST_CASES = 5
MIN_TEST_STEPS = 2
REQUIRE_UNIQUE_TESTCASE_IDS = True
REQUIRE_UNIQUE_DESCRIPTIONS = True

# Overall coverage quality gate.
MIN_COVERAGE_PERCENTAGE = 90
COVERAGE_MATCH_THRESHOLD = 0.50


#---------------- DeepEval Thresholds-------------------
HALLUCINATION_THRESHOLD = 0.20
CORRECTNESS_THRESHOLD = 0.90
COMPLETENESS_THRESHOLD = 0.90
RELEVANCY_THRESHOLD = 0.80
BUSINESS_RULE_THRESHOLD = 0.90
REQUIREMENT_THRESHOLD = 0.90

#-----------------Score Weights-------------------------
SCHEMA_WEIGHT = 0.15
TESTCASE_WEIGHT = 0.25
COVERAGE_WEIGHT = 0.30
DEEPEVAL_WEIGHT = 0.30


#-----------------Execution Config----------------
# Evaluation
MAX_TESTCASES_PER_BATCH = 25

# Parallel Execution
MAX_CONCURRENT_REQUESTS = 3

# Retry Policy
MAX_RETRIES = 3
REQUEST_TIMEOUT = 300

# Logging
SHOW_CONSOLE_LOGS = True

# Smoke Test
MAX_REQUIREMENTS = None
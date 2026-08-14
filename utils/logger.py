from datetime import datetime

# Timestamp
def _timestamp():
    """Return current timestamp."""
    return datetime.now().strftime("%H:%M:%S")

# Basic Logger
def blank(): print()
def separator(): print("-" * 100)
def header(title: str):
    line = "=" * 100
    print(f"\n{line}")
    print(title)
    print(line)

def info(message: str): print(f"[{_timestamp()}] {message}")
def success(message: str): print(f"[{_timestamp()}] ✓ {message}")
def warning(message: str): print(f"[{_timestamp()}] ⚠ {message}")
def failed(message: str): 
    message = str(message)
    if "RESOURCE_EXHAUSTED" in message: message = ("Gemini API quota exhausted.")
    print(f"[{_timestamp()}] ✗ {message}")

# Evaluation Summary
def evaluation_summary(result: dict):
    """
    Print the standardized DeepEval evaluation result.

    Expected result structure:
    result
    ├── generator
    ├── requirement
    ├── generated_output
    ├── benchmark_repository
    ├── testcase_quality_validation
    │   ├── schema
    │   ├── testcase
    │   └── coverage
    ├── deepeval_evaluation
    └── overall
    """

    requirement = result.get(
        "requirement",
        {},
    )

    validation = result.get(
        "testcase_quality_validation",
        {},
    )

    deepeval_evaluation = result.get(
        "deepeval_evaluation",
        {},
    )

    overall = result.get(
        "overall",
        {},
    )

    # ==========================================================
    # Requirement
    # ==========================================================

    separator()

    print("LLM Evaluation Summary")

    separator()

    print(
        f"Generator             : "
        f"{result.get('generator', '')}"
    )

    print(
        f"Requirement ID        : "
        f"{requirement.get('id', '')}"
    )

    print(
        f"Requirement Type      : "
        f"{requirement.get('type', '')}"
    )

    print(
        f"Requirement Title     : "
        f"{requirement.get('title', '')}"
    )

    print(
        f"Priority              : "
        f"{requirement.get('priority', '')}"
    )

    # ==========================================================
    # Test Case Quality Validation
    # ==========================================================

    separator()

    print("Test Case Quality Validation")

    separator()

    # ----------------------------------------------------------
    # Schema
    # ----------------------------------------------------------

    schema = validation.get(
        "schema",
        {},
    )

    print(
        f"Schema Validation     : "
        f"{schema.get('score', 0)}%"
    )

    # ----------------------------------------------------------
    # Test Case
    # ----------------------------------------------------------

    testcase = validation.get(
        "testcase",
        {},
    )

    print(
        f"TestCase Validation   : "
        f"{testcase.get('score', 0)}%"
    )

    # ----------------------------------------------------------
    # Coverage
    # ----------------------------------------------------------

    coverage = validation.get(
        "coverage",
        {},
    )

    print(
        f"Coverage Validation   : "
        f"{coverage.get('score', 0)}%"
    )

    # ==========================================================
    # Coverage Statistics
    # ==========================================================

    statistics = coverage.get(
        "statistics",
        {},
    )

    if statistics:

        print("\nCoverage Statistics")

        for key, value in statistics.items():

            formatted_key = (
                key
                .replace("_", " ")
                .title()
            )

            print(
                f"   {formatted_key:<30}: "
                f"{value}"
            )

    # ==========================================================
    # Coverage Errors
    # ==========================================================

    if coverage.get("errors"):

        print("\nCoverage Errors")

        for error in coverage["errors"]:

            print(
                f"   ✗ {error}"
            )

    # ==========================================================
    # Coverage Warnings
    # ==========================================================

    if coverage.get("warnings"):

        print("\nCoverage Warnings")

        for warning_message in coverage["warnings"]:

            print(
                f"   ⚠ {warning_message}"
            )

    # ==========================================================
    # DeepEval Evaluation
    # ==========================================================

    separator()

    print("DeepEval Evaluation")

    separator()

    metrics = [

        (
            "Hallucination",
            "hallucination",
        ),

        (
            "Correctness",
            "correctness",
        ),

        (
            "Completeness",
            "completeness",
        ),


        (
            "Business Rule",
            "business_rule",
        ),

        (
            "Requirement",
            "requirement",
        ),

        (
            "Answer Relevancy",
            "answer_relevancy",
        ),

    ]

    for title, key in metrics:

        if key not in deepeval_evaluation:

            continue

        metric = deepeval_evaluation.get(
            key,
            {},
        )

        score = metric.get(
            "score",
            0,
        )

        risk = metric.get(
            "risk"
        )

        if risk is None:

            print(
                f"{title:<25}: "
                f"{score}%"
            )

        else:

            print(
                f"{title:<25}: "
                f"{score}% "
                f"(Risk {risk}%)"
            )

    # ==========================================================
    # DeepEval Overall Score
    # ==========================================================

    print(
        f"{'DeepEval Score':<25}: "
        f"{deepeval_evaluation.get('score', 0)}%"
    )

    # ==========================================================
    # Judge Model
    # ==========================================================

    if deepeval_evaluation.get(
        "judge_model"
    ):

        print(
            f"{'Judge Model':<25}: "
            f"{deepeval_evaluation.get('judge_model')}"
        )

    # ==========================================================
    # Overall Evaluation
    # ==========================================================

    separator()

    print("Overall Evaluation")

    separator()

    print(
        f"Quality Validation     : "
        f"{overall.get('quality_validation_score', 0)}%"
    )

    print(
        f"DeepEval Evaluation    : "
        f"{overall.get('deepeval_evaluation_score', 0)}%"
    )

    print(
        f"Overall Quality        : "
        f"{overall.get('overall_score', 0)}%"
    )

    print(
        f"Status                 : "
        f"{overall.get('status', '')}"
    )

    print(
        f"Execution Time         : "
        f"{overall.get('execution_time', 0)} sec"
    )

    if overall.get("winner"):

        print(
            f"Winner                 : "
            f"{overall.get('winner')}"
        )

    separator()
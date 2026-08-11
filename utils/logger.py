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
    if "RESOURCE_EXHAUSTED" in message: message = "Gemini API quota exhausted."
    print(f"[{_timestamp()}] ✗ {message}")


# Evaluation Summary
def evaluation_summary(result: dict):
    """
    Print the standardized evaluation result.

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
    ├── deepeval
    └── overall
    """

    requirement = result.get("requirement",{},)
    validation = result.get("testcase_quality_validation",{},)
    deepeval = result.get("deepeval",{},)
    overall = result.get("overall",{},)

    # Header
    separator()
    print("LLM Evaluation Summary")
    separator()

    print(f"Generator             : "f"{result.get('generator', '')}")
    print(f"Requirement ID        : "f"{requirement.get('id', '')}")
    print(f"Requirement Type      : "f"{requirement.get('type', '')}")
    print(f"Requirement Title     : "f"{requirement.get('title', '')}")
    print(f"Priority              : "f"{requirement.get('priority', '')}")

    # Test Case Quality Validation
    separator()
    print("Test Case Quality Validation")
    separator()

    # Schema
    schema = validation.get("schema",{},)
    print(f"Schema Validation     : "f"{schema.get('score', 0)}%")

    
    # Test Case
    testcase = validation.get(
        "testcase",
        {},
    )

    print(
        f"TestCase Validation   : "
        f"{testcase.get('score', 0)}%"
    )

    
    # Coverage
    

    coverage = validation.get(
        "coverage",
        {},
    )

    print(
        f"Coverage Validation   : "
        f"{coverage.get('score', 0)}%"
    )

    
    # Coverage Scenarios
    

    if coverage.get("covered"):

        print(
            f"\nCovered Scenarios "
            f"({len(coverage['covered'])})"
        )

        for scenario in coverage["covered"]:

            print(
                f"   ✓ {scenario}"
            )

    if coverage.get("missing"):

        print(
            f"\nMissing Scenarios "
            f"({len(coverage['missing'])})"
        )

        for scenario in coverage["missing"]:

            print(
                f"   ✗ {scenario}"
            )

    if coverage.get("additional"):

        print(
            f"\nAdditional Scenarios "
            f"({len(coverage['additional'])})"
        )

        for scenario in coverage["additional"]:

            print(
                f"   + {scenario}"
            )

    
    # Coverage Errors
    

    if coverage.get("errors"):

        print("\nCoverage Errors")

        for error in coverage["errors"]:

            print(
                f"   ✗ {error}"
            )

    
    # Coverage Warnings
    

    if coverage.get("warnings"):

        print("\nCoverage Warnings")

        for warning_message in coverage["warnings"]:

            print(
                f"   ⚠ {warning_message}"
            )

    # ======================================================
    # AI Evaluation
    # ======================================================

    separator()

    print("AI Evaluation")

    separator()

    metrics = [

        ("Hallucination", "hallucination"),

        ("Correctness", "correctness"),

        ("Faithfulness", "faithfulness"),

        ("Completeness", "completeness"),

        ("Context Precision", "context_precision"),

        ("Context Recall", "context_recall"),

        ("Business Rule", "business_rule"),

        ("Requirement", "requirement"),

        ("Answer Relevancy", "answer_relevancy"),

    ]

    for title, key in metrics:

        if key not in deepeval:
            continue

        metric = deepeval.get(
            key,
            {},
        )

        free = metric.get(
            "free",
            metric.get(
                "score",
                0,
            ),
        )

        risk = metric.get(
            "risk"
        )

        if risk is None:

            print(
                f"{title:<25}: "
                f"{free}%"
            )

        else:

            print(
                f"{title:<25}: "
                f"{free}% "
                f"(Risk {risk}%)"
            )

    
    # AI Overall Score
    

    print(
        f"{'AI Evaluation Score':<25}: "
        f"{deepeval.get('score', 0)}%"
    )

    
    # Judge Model
    

    if deepeval.get("judge_model"):

        print(
            f"{'Judge Model':<25}: "
            f"{deepeval.get('judge_model')}"
        )

    # ======================================================
    # Overall Evaluation
    # ======================================================

    separator()

    print("Overall Evaluation")

    separator()

    print(
        f"Quality Validation     : "
        f"{overall.get('quality_validation_score', 0)}%"
    )

    print(
        f"AI Evaluation          : "
        f"{overall.get('ai_evaluation_score', 0)}%"
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


# Validation Details

def print_validation(
    name: str,
    validation_result: dict,
):
    """
    Print detailed validation information.
    """

    print(f"\n{name}")

    separator()

    print(
        f"Status : "
        f"{validation_result.get('status', '')}"
    )

    print(
        f"Score  : "
        f"{validation_result.get('score', 0)}%"
    )

    
    # Errors
    

    if validation_result.get("errors"):

        print("\nErrors")

        for error in validation_result["errors"]:

            print(
                f"  • {error}"
            )

    
    # Warnings
    

    if validation_result.get("warnings"):

        print("\nWarnings")

        for warning_message in validation_result["warnings"]:

            print(
                f"  • {warning_message}"
            )

    separator()
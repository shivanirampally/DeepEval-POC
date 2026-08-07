from datetime import datetime


# ==========================================================
# Timestamp
# ==========================================================

def _timestamp():
    return datetime.now().strftime("%H:%M:%S")


# ==========================================================
# Basic Logger
# ==========================================================

def blank():
    print()


def separator():
    print("-" * 100)


def header(title: str):

    line = "=" * 100

    print(f"\n{line}")

    print(title)

    print(line)


def info(message: str):
    print(f"[{_timestamp()}] {message}")


def success(message: str):
    print(f"[{_timestamp()}] ✓ {message}")


def warning(message: str):
    print(f"[{_timestamp()}] ⚠ {message}")


def failed(message: str):

    if "RESOURCE_EXHAUSTED" in message:
        message = "Gemini API quota exhausted."

    print(f"[{_timestamp()}] ✗ {message}")


# ==========================================================
# Evaluation Summary
# ==========================================================

def evaluation_summary(result: dict):

    separator()
    print("LLM Evaluation Summary")
    separator()

    print(f"Generator             : {result['generator']}")
    print(f"Requirement ID        : {result['requirementId']}")
    print(f"Requirement Title     : {result['title']}")

    separator()
    print("Quality Validation")
    separator()

    print(f"Schema Validation     : {result['schemaValidation']['score']}%")
    print(f"TestCase Validation   : {result['testCaseValidation']['score']}%")
    print(f"Coverage Validation   : {result['coverageValidation']['score']}%")

    coverage = result["coverageValidation"]

    if coverage.get("covered"):
        print(f"\nCovered Scenarios ({len(coverage['covered'])})")

        for item in coverage["covered"]:
            print(f"  ✓ {item}")

    if coverage.get("missing"):
        print(f"\nMissing Scenarios ({len(coverage['missing'])})")

        for item in coverage["missing"]:
            print(f"  ✗ {item}")

    if coverage.get("additional"):
        print(f"\nAdditional Scenarios ({len(coverage['additional'])})")

        for item in coverage["additional"]:
            print(f"  + {item}")

    separator()
    print("AI Evaluation")
    separator()

    deepeval = result["deepEval"]

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

        if key in deepeval:

            metric = deepeval[key]

            print(
                f"{title:<24}: "
                f"{metric.get('free', metric.get('score', 0))}%"
            )

    separator()
    print("Overall Evaluation")
    separator()

    overall = result["overall"]

    print(
        f"Quality Validation    : "
        f"{overall['quality_validation_score']}%"
    )

    print(
        f"AI Evaluation         : "
        f"{overall['ai_evaluation_score']}%"
    )

    print(
        f"Overall Quality       : "
        f"{overall['overall_score']}%"
    )

    print(
        f"Status                : "
        f"{overall['status']}"
    )

    print(
        f"Execution Time        : "
        f"{overall.get('execution_time',0)} sec"
    )

    separator()


# ==========================================================
# Validation Details
# ==========================================================

def print_validation(
    name: str,
    validation_result: dict,
):

    print(f"\n{name}")

    separator()

    print(
        f"Status : {validation_result['status']}"
    )

    print(
        f"Score  : {validation_result['score']}%"
    )

    if validation_result.get("errors"):

        print("\nErrors")

        for error in validation_result["errors"]:

            print(f"  • {error}")

    if validation_result.get("warnings"):

        print("\nWarnings")

        for warning_message in validation_result["warnings"]:

            print(f"  • {warning_message}")

    separator()
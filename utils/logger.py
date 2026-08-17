from datetime import datetime


# ==========================================================
# TIMESTAMP
# ==========================================================

def _timestamp():
    """Return current timestamp."""
    return datetime.now().strftime("%H:%M:%S")


# ==========================================================
# BASIC LOGGER
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

    print(
        f"[{_timestamp()}] {message}"
    )


def success(message: str):

    print(
        f"[{_timestamp()}] ✓ {message}"
    )


def warning(message: str):

    print(
        f"[{_timestamp()}] ⚠ {message}"
    )


def failed(message: str):

    message = str(message)

    if "RESOURCE_EXHAUSTED" in message:

        message = (
            "Gemini API quota exhausted."
        )

    print(
        f"[{_timestamp()}] ✗ {message}"
    )


# ==========================================================
# HELPER
# ==========================================================

def _print_metric(
    title,
    metric,
    *,
    inverse=False,
):
    """
    Print a metric using a consistent business-friendly format.

    Normal metrics:
        Correctness
        Correctness Gap

    Inverse metric:
        Hallucination
        Hallucination-Free
    """

    if not isinstance(metric, dict):
        return

    score = metric.get(
        "score",
        0,
    )

    # ------------------------------------------------------
    # Hallucination
    # ------------------------------------------------------

    if inverse:

        risk = metric.get(
            "risk",
            metric.get(
                "gap",
                round(
                    100 - score,
                    2,
                ),
            ),
        )

        hallucination_free = metric.get(
            "score",
            round(
                100 - risk,
                2,
            ),
        )

        print(
            f"{'Hallucination':<25}: "
            f"{risk}%"
        )

        print(
            f"{'Hallucination-Free':<25}: "
            f"{hallucination_free}%"
        )

        return

    # ------------------------------------------------------
    # Normal Metric
    # ------------------------------------------------------

    gap = metric.get(
        "gap",
        None,
    )

    print(
        f"{title:<25}: "
        f"{score}%"
    )

    if gap is not None:

        print(
            f"{title + ' Gap':<25}: "
            f"{gap}%"
        )


# ==========================================================
# EVALUATION SUMMARY
# ==========================================================

def evaluation_summary(result: dict):
    """
    Print the standardized evaluation result.

    Evaluation structure:

    Framework Validation
        ├── Schema
        ├── Test Case
        └── Coverage

    DeepEval - Benchmark
        ├── Hallucination
        ├── Correctness
        ├── Completeness
        ├── Business Rule Coverage
        ├── Requirement Satisfaction
        └── Answer Relevancy

    DeepEval - Requirement Only
        ├── Hallucination
        ├── Answer Relevancy
        └── Requirement Alignment

    The two DeepEval modes are intentionally displayed
    separately so that Requirement-Only evaluation is not
    confused with framework coverage validation.
    """

    requirement = result.get(
        "requirement",
        {},
    )

    validation = result.get(
        "testcase_quality_validation",
        {},
    )

    # ------------------------------------------------------
    # Benchmark DeepEval
    # ------------------------------------------------------

    benchmark = result.get(
        "deepeval_evaluation",
        {},
    )

    # ------------------------------------------------------
    # Requirement-Only DeepEval
    # ------------------------------------------------------

    requirement_only = result.get(
        "requirement_only_evaluation",
        {},
    )

    overall = result.get(
        "overall",
        {},
    )

    # ==========================================================
    # REQUIREMENT SUMMARY
    # ==========================================================

    separator()

    print(
        "LLM Evaluation Summary"
    )

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
    # 1. FRAMEWORK VALIDATION
    # ==========================================================

    separator()

    print(
        "FRAMEWORK VALIDATION"
    )

    separator()

    schema = validation.get(
        "schema",
        {},
    )

    testcase = validation.get(
        "testcase",
        {},
    )

    coverage = validation.get(
        "coverage",
        {},
    )

    print(
        f"{'Schema Validation':<25}: "
        f"{schema.get('score', 0)}%"
    )

    print(
        f"{'Test Case Validation':<25}: "
        f"{testcase.get('score', 0)}%"
    )

    print(
        f"{'Coverage Validation':<25}: "
        f"{coverage.get('score', 0)}%"
    )

    # ==========================================================
    # COVERAGE DETAILS
    # ==========================================================

    statistics = coverage.get(
        "statistics",
        {},
    )

    if statistics:

        print(
            "\nCoverage Statistics"
        )

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
    # COVERAGE ERRORS
    # ==========================================================

    if coverage.get("errors"):

        print(
            "\nCoverage Errors"
        )

        for error in coverage["errors"]:

            print(
                f"   ✗ {error}"
            )

    # ==========================================================
    # COVERAGE WARNINGS
    # ==========================================================

    if coverage.get("warnings"):

        print(
            "\nCoverage Warnings"
        )

        for warning_message in coverage["warnings"]:

            print(
                f"   ⚠ {warning_message}"
            )

    # ==========================================================
    # 2. DEEPEVAL - BENCHMARK
    # ==========================================================

    separator()

    print(
        "DEEPEVAL - BENCHMARK EVALUATION"
    )

    print(
        "Generated test cases are evaluated "
        "against the benchmark / ground truth."
    )

    separator()

    if benchmark:

        # ------------------------------------------------------
        # Hallucination
        # ------------------------------------------------------

        _print_metric(
            "Hallucination",
            benchmark.get(
                "hallucination",
                {},
            ),
            inverse=True,
        )

        # ------------------------------------------------------
        # Correctness
        # ------------------------------------------------------

        _print_metric(
            "Correctness",
            benchmark.get(
                "correctness",
                {},
            ),
        )

        # ------------------------------------------------------
        # Completeness
        # ------------------------------------------------------

        _print_metric(
            "Completeness",
            benchmark.get(
                "completeness",
                {},
            ),
        )

        # ------------------------------------------------------
        # Business Rule
        # ------------------------------------------------------

        business_rule = benchmark.get(
            "business_rule",
            {},
        )

        print(
            f"{'Business Rule Coverage':<25}: "
            f"{business_rule.get('score', 0)}%"
        )

        print(
            f"{'Business Rule Failed':<25}: "
            f"{business_rule.get('gap', 0)}%"
        )

        # ------------------------------------------------------
        # Requirement Satisfaction
        # ------------------------------------------------------

        requirement_metric = benchmark.get(
            "requirement",
            {},
        )

        print(
            f"{'Requirement Satisfaction':<25}: "
            f"{requirement_metric.get('score', 0)}%"
        )

        print(
            f"{'Requirement Unsatisfied':<25}: "
            f"{requirement_metric.get('gap', 0)}%"
        )

        # ------------------------------------------------------
        # Answer Relevancy
        # ------------------------------------------------------

        answer_relevancy = benchmark.get(
            "answer_relevancy",
            {},
        )

        print(
            f"{'Answer Relevancy':<25}: "
            f"{answer_relevancy.get('score', 0)}%"
        )

        print(
            f"{'Answer Irrelevancy':<25}: "
            f"{answer_relevancy.get('gap', 0)}%"
        )

        # ------------------------------------------------------
        # DeepEval Score
        # ------------------------------------------------------

        print()

        print(
            f"{'DeepEval Score':<25}: "
            f"{benchmark.get('score', 0)}%"
        )

        # ------------------------------------------------------
        # Evaluator
        # ------------------------------------------------------

        evaluator_model = benchmark.get(
            "evaluator_model",
            benchmark.get(
                "judge_model",
                "",
            ),
        )

        if evaluator_model:

            print(
                f"{'Evaluator':<25}: "
                f"{evaluator_model}"
            )

    else:

        print(
            "Benchmark evaluation was not executed."
        )

    # ==========================================================
    # 3. DEEPEVAL - REQUIREMENT ONLY
    # ==========================================================

    separator()

    print(
        "DEEPEVAL - REQUIREMENT-ONLY EVALUATION"
    )

    print(
        "Generated test cases are evaluated "
        "against the requirement without benchmark "
        "test cases."
    )

    separator()

    if requirement_only:

        # ------------------------------------------------------
        # IMPORTANT:
        # NO COVERAGE HERE
        # ------------------------------------------------------

        # Hallucination

        _print_metric(
            "Hallucination",
            requirement_only.get(
                "hallucination",
                {},
            ),
            inverse=True,
        )

        # Answer Relevancy

        answer_relevancy = (
            requirement_only.get(
                "answer_relevancy",
                {},
            )
        )

        print(
            f"{'Answer Relevancy':<25}: "
            f"{answer_relevancy.get('score', 0)}%"
        )

        print(
            f"{'Answer Irrelevancy':<25}: "
            f"{answer_relevancy.get('gap', 0)}%"
        )

        # Requirement Alignment

        requirement_quality = (
            requirement_only.get(
                "requirement_quality",
                {},
            )
        )

        print(
            f"{'Requirement Satisfaction':<25}: "
            f"{requirement_quality.get('score', 0)}%"
        )

        print(
            f"{'Requirement Unsatisfied':<25}: "
            f"{requirement_quality.get('gap', 0)}%"
        )

        # Requirement-Only Score

        print()

        print(
            f"{'Requirement-Only Score':<25}: "
            f"{requirement_only.get('score', 0)}%"
        )

        # Evaluator

        evaluator_model = (
            requirement_only.get(
                "evaluator_model",
                requirement_only.get(
                    "judge_model",
                    "",
                ),
            )
        )

        if evaluator_model:

            print(
                f"{'Evaluator':<25}: "
                f"{evaluator_model}"
            )

        # ------------------------------------------------------
        # Findings
        # ------------------------------------------------------

        findings = requirement_only.get(
            "findings",
            [],
        )

        if findings:

            print(
                "\nRequirement-Only Findings"
            )

            for finding in findings:

                print(
                    f"   ⚠ {finding}"
                )

    else:

        print(
            "Requirement-Only evaluation was not executed."
        )

    # ==========================================================
    # 4. OVERALL EVALUATION
    # ==========================================================

    separator()

    print(
        "OVERALL EVALUATION"
    )

    separator()

    print(
        f"{'Quality Validation':<25}: "
        f"{overall.get('quality_validation_score', 0)}%"
    )

    print(
        f"{'Benchmark DeepEval':<25}: "
        f"{overall.get('deepeval_evaluation_score', 0)}%"
    )

    print(
        f"{'Overall Quality':<25}: "
        f"{overall.get('overall_score', 0)}%"
    )

    print(
        f"{'Status':<25}: "
        f"{overall.get('status', '')}"
    )

    print(
        f"{'Execution Time':<25}: "
        f"{overall.get('execution_time', 0)} sec"
    )

    if overall.get("winner"):

        print(
            f"{'Winner':<25}: "
            f"{overall.get('winner')}"
        )

    separator()
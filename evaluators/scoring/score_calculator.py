from config.settings import (
    SCHEMA_WEIGHT,
    TESTCASE_WEIGHT,
    COVERAGE_WEIGHT,
    DEEPEVAL_WEIGHT,
)


class ScoreCalculator:
    """
    Calculates the final evaluation scores.

    All incoming scores must be normalized to
    percentages from 0 to 100.
    """

    WEIGHTS = {
        "schema": SCHEMA_WEIGHT,
        "testcase": TESTCASE_WEIGHT,
        "coverage": COVERAGE_WEIGHT,
        "deepeval": DEEPEVAL_WEIGHT,
    }

    @classmethod
    def calculate(
        cls,
        schema_result,
        testcase_result,
        coverage_result,
        deepeval_result,
    ):
        schema_score = schema_result.get("score", 0)
        testcase_score = testcase_result.get("score", 0)
        coverage_score = coverage_result.get("score", 0)
        deepeval_score = deepeval_result.get("score", 0)

        framework_weight = (
            SCHEMA_WEIGHT
            + TESTCASE_WEIGHT
            + COVERAGE_WEIGHT
        )

        quality_validation_score = round(
            (
                schema_score * SCHEMA_WEIGHT
                + testcase_score * TESTCASE_WEIGHT
                + coverage_score * COVERAGE_WEIGHT
            ) / framework_weight,
            2,
        )

        overall_score = round(
            schema_score * SCHEMA_WEIGHT
            + testcase_score * TESTCASE_WEIGHT
            + coverage_score * COVERAGE_WEIGHT
            + deepeval_score * DEEPEVAL_WEIGHT,
            2,
        )

        if overall_score >= 90:
            status = "PASS"
        elif overall_score >= 75:
            status = "REVIEW"
        else:
            status = "FAIL"

        return {
            "quality_validation_score": (
                quality_validation_score
            ),
            "deepeval_evaluation_score": (
                round(deepeval_score, 2)
            ),
            "overall_score": overall_score,
            "status": status,
            "execution_time": 0,
            "winner": "",
        }
from config.settings import (
    SCHEMA_WEIGHT,
    TESTCASE_WEIGHT,
    COVERAGE_WEIGHT,
    DEEPEVAL_WEIGHT,
)


class ScoreCalculator:
    """
    Calculates Enterprise Quality Scores.

    All incoming scores must already be
    normalized to percentages (0-100).
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

        # -------------------------------------------------
        # Framework Scores
        # -------------------------------------------------

        schema_score = schema_result.get(
            "score",
            0,
        )

        testcase_score = testcase_result.get(
            "score",
            0,
        )

        coverage_score = coverage_result.get(
            "score",
            0,
        )

        # -------------------------------------------------
        # AI Evaluation Score
        # -------------------------------------------------

        ai_score = deepeval_result.get(
            "score",
            0,
        )

        # -------------------------------------------------
        # Quality Validation Score
        # -------------------------------------------------

        quality_validation_score = round(

            (

                schema_score +

                testcase_score +

                coverage_score

            ) / 3,

            2,

        )

        # -------------------------------------------------
        # Overall Score
        # -------------------------------------------------

        overall_score = round(

            (

                schema_score *

                cls.WEIGHTS["schema"]

                +

                testcase_score *

                cls.WEIGHTS["testcase"]

                +

                coverage_score *

                cls.WEIGHTS["coverage"]

                +

                ai_score *

                cls.WEIGHTS["deepeval"]

            ),

            2,

        )

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        if overall_score >= 90:

            status = "PASS"

        elif overall_score >= 75:

            status = "REVIEW"

        else:

            status = "FAIL"

        # -------------------------------------------------
        # Final Result
        # -------------------------------------------------

        return {

            "quality_validation_score":

                quality_validation_score,

            "ai_evaluation_score":

                round(ai_score, 2),

            "overall_score":

                overall_score,

            "status":

                status,

            "execution_time":

                0,

            "winner":

                "",

        }
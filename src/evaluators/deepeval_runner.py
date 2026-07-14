from deepeval.metrics import (
    HallucinationMetric,
    AnswerRelevancyMetric,
    GEval
)

from deepeval.test_case import (
    LLMTestCase,
    LLMTestCaseParams
)

from deepeval.models import GeminiModel

from config.settings import (
    GEMINI_API_KEY,
    DEEPEVAL_GEMINI_MODEL
)


class DeepEvalRunner:
    """
    Executes DeepEval metrics against AI responses.
    """

    # Gemini Judge Model (initialized once)
    gemini_model = GeminiModel(
        model=DEEPEVAL_GEMINI_MODEL,
        api_key=GEMINI_API_KEY
    )

    @staticmethod
    def evaluate(
        prompt,
        expected_output,
        actual_output,
        context=""
    ):

        # -----------------------------
        # Normalize Input Values
        # -----------------------------
        prompt = str(prompt).strip()

        expected_output = (
            "" if expected_output is None
            else str(expected_output).strip()
        )

        actual_output = (
            "" if actual_output is None
            else str(actual_output).strip()
        )

        context_list = []

        if (
            context is not None
            and str(context).strip() != ""
            and str(context).lower() != "nan"
        ):
            context_list.append(str(context).strip())

        # -----------------------------
        # Create Test Case
        # -----------------------------
        test_case = LLMTestCase(
            input=prompt,
            actual_output=actual_output,
            expected_output=expected_output,
            context=context_list
        )

        # -----------------------------
        # Initialize Metrics
        # -----------------------------
        hallucination_metric = HallucinationMetric(
            model=DeepEvalRunner.gemini_model,
            threshold=0.5,
            include_reason=True,
            verbose_mode=False
        )

        answer_metric = AnswerRelevancyMetric(
            model=DeepEvalRunner.gemini_model,
            threshold=0.5,
            include_reason=True,
            verbose_mode=False
        )

        correctness_metric = GEval(
            name="Correctness",
            criteria="""
            Evaluate whether the AI response is factually correct
            and satisfies the expected output.

            Give a high score if the response is accurate,
            complete and aligned with the expected answer.
            Give a low score if it contains incorrect,
            fabricated or contradictory information.
            """,
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.EXPECTED_OUTPUT
            ],
            model=DeepEvalRunner.gemini_model,
            threshold=0.5
        )

        # -----------------------------
        # Execute Metrics
        # -----------------------------
        hallucination_metric.measure(test_case)
        answer_metric.measure(test_case)
        correctness_metric.measure(test_case)

        # -----------------------------
        # Overall Result
        # -----------------------------
        result = "Passed"

        if (
            hallucination_metric.score > 0.5
            or answer_metric.score < 0.5
            or correctness_metric.score < 0.5
        ):
            result = "Failed"

        # -----------------------------
        # Remarks
        # -----------------------------
        remarks = []

        if hallucination_metric.reason:
            remarks.append(
                f"Hallucination: {hallucination_metric.reason}"
            )

        if answer_metric.reason:
            remarks.append(
                f"Answer Relevancy: {answer_metric.reason}"
            )

        if correctness_metric.reason:
            remarks.append(
                f"Correctness: {correctness_metric.reason}"
            )

        # -----------------------------
        # Return Evaluation
        # -----------------------------
        return {
            "hallucination_score": round(
                hallucination_metric.score,
                2
            ),

            "answer_relevancy_score": round(
                answer_metric.score,
                2
            ),

            "correctness_score": round(
                correctness_metric.score,
                2
            ),

            "result": result,

            "remarks": " | ".join(remarks)
        }
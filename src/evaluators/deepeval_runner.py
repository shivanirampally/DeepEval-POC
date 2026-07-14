from deepeval.metrics import (
    HallucinationMetric,
    AnswerRelevancyMetric
)

from deepeval.test_case import (
    LLMTestCase
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

    # Initialize Gemini Judge Model only once
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

        test_case = LLMTestCase(
            input=prompt,
            actual_output=actual_output,
            expected_output=expected_output,
            context=[context] if context else []
        )

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

        hallucination_metric.measure(test_case)
        answer_metric.measure(test_case)

        result = "Passed"

        if (
            hallucination_metric.score > 0.5
            or
            answer_metric.score < 0.5
        ):
            result = "Failed"

        remarks = []

        if hallucination_metric.reason:
            remarks.append(
                f"Hallucination: {hallucination_metric.reason}"
            )

        if answer_metric.reason:
            remarks.append(
                f"Answer Relevancy: {answer_metric.reason}"
            )

        return {

            "hallucination_score":
                round(
                    hallucination_metric.score,
                    2
                ),

            "answer_relevancy_score":
                round(
                    answer_metric.score,
                    2
                ),

            "result":
                result,

            "remarks":
                " | ".join(remarks)
        }
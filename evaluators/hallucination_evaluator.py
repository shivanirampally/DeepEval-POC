from deepeval.metrics import (
    HallucinationMetric,
    AnswerRelevancyMetric,
    GEval,
)

from deepeval.test_case import (
    LLMTestCase,
    LLMTestCaseParams,
)

from config.app_config import (
    HALLUCINATION_THRESHOLD,
    RELEVANCY_THRESHOLD,
)

from config.gemini_config import load_gemini_model
from config.prompts import CORRECTNESS_CRITERIA

from utils.logger import (
    info,
    success,
    failed,
)


class HallucinationEvaluator:

    def __init__(self):

        judge = load_gemini_model()

        self.hallucination = HallucinationMetric(
            threshold=HALLUCINATION_THRESHOLD,
            model=judge,
        )

        self.relevancy = AnswerRelevancyMetric(
            threshold=RELEVANCY_THRESHOLD,
            model=judge,
        )

        self.correctness = GEval(
            name="Correctness",
            criteria=CORRECTNESS_CRITERIA,
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.EXPECTED_OUTPUT,
            ],
            model=judge,
        )

    def evaluate(
        self,
        input_text,
        actual_output_text,
        context,
        expected_output,
    ):

        test_case = LLMTestCase(
            input=input_text,
            actual_output=actual_output_text,
            expected_output=expected_output,
            context=context,
        )

        try:

            info("Running Hallucination Metric...")
            self.hallucination.measure(test_case)
            success("Hallucination Completed")

            info("Running Correctness Metric...")
            self.correctness.measure(test_case)
            success("Correctness Completed")

            info("Running Answer Relevancy Metric...")
            self.relevancy.measure(test_case)
            success("Answer Relevancy Completed")

            return {
                "status": "SUCCESS",
                "hallucination_score": self.hallucination.score,
                "hallucination_reason": self.hallucination.reason,
                "answer_relevancy_score": self.relevancy.score,
                "answer_relevancy_reason": self.relevancy.reason,
                "correctness_score": self.correctness.score,
                "correctness_reason": self.correctness.reason,
            }

        except Exception as e:

            error = str(e)

            failed(error)

            return {
                "status": "FAILED",
                "error": error,
                "hallucination_score": None,
                "hallucination_reason": error,
                "answer_relevancy_score": None,
                "answer_relevancy_reason": error,
                "correctness_score": None,
                "correctness_reason": error,
            }
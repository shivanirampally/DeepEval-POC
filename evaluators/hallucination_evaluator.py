from deepeval.metrics import (
    HallucinationMetric,
    AnswerRelevancyMetric,
    GEval,
)

from deepeval.test_case import (
    LLMTestCase,
    LLMTestCaseParams,
)

from config.gemini_config import load_model


class HallucinationEvaluator:

    def __init__(self):

        judge = load_model()

        self.hallucination = HallucinationMetric(
            threshold=0.2,
            model=judge
        )

        self.relevancy = AnswerRelevancyMetric(
            threshold=0.5,
            model=judge
        )

        self.correctness = GEval(
        name="Correctness",
        criteria="""
            Determine whether the actual output correctly answers the user's question
            and matches the expected output.

            A high score should be given when the actual output is semantically
            equivalent to the expected output, even if the wording differs.
            """,
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
        context_text,
        expected_output
    ):

        test_case = LLMTestCase(
            input=input_text,
            actual_output=actual_output_text,
            expected_output=expected_output,
            context=context_text
        )

        self.hallucination.measure(test_case)
        self.relevancy.measure(test_case)
        self.correctness.measure(test_case)

        return {
            "hallucination_score": self.hallucination.score,
            "hallucination_reason": self.hallucination.reason,
            "answer_relevancy_score": self.relevancy.score,
            "answer_relevancy_reason": self.relevancy.reason,
            "correctness_score": self.correctness.score,
            "correctness_reason": self.correctness.reason,
        }
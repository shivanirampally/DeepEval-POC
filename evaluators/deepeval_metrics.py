import json
from deepeval.test_case import LLMTestCase
from config.judge_settings import OllamaJudge
from evaluators.metrics.hallucination_metric import (
    HallucinationEvaluator,
)

from evaluators.metrics.correctness_metric import (
    CorrectnessEvaluator,
)

from evaluators.metrics.answer_relevancy_metric import (
    AnswerRelevancyEvaluator,
)

from parsers.benchmark_repository_parser import (
    BenchmarkRepositoryParser,
)

from utils.logger import (
    info,
    success,
    failed,
)


class DeepEvalMetrics:
    """
    Executes all DeepEval semantic metrics.

    Responsibilities
    ----------------
    • Build DeepEval test case
    • Execute semantic metrics
    • Aggregate scores
    """

    def __init__(self):

        judge = OllamaJudge()

        self.hallucination = HallucinationEvaluator(
            judge
        )

        self.correctness = CorrectnessEvaluator(
            judge
        )

        self.answer_relevancy = (
            AnswerRelevancyEvaluator(
                judge
            )
        )

    # ==========================================================
    # Evaluate
    # ==========================================================

    def evaluate(
        self,
        *,
        requirement,
        generated_output,
    ):

        # ------------------------------------------------------
        # Generated Output
        # ------------------------------------------------------

        actual_output = json.dumps(
            generated_output,
            indent=2,
            ensure_ascii=False,
        )

        # ------------------------------------------------------
        # Benchmark Repository
        # ------------------------------------------------------

        benchmark_output = (
            BenchmarkRepositoryParser.to_benchmark_text(
                requirement.benchmark_repository
            )
        )

        # ------------------------------------------------------
        # DeepEval Test Case
        # ------------------------------------------------------

        test_case = LLMTestCase(

            input=requirement.description,

            actual_output=actual_output,

            expected_output=benchmark_output,

            context=[
                requirement.description,
                requirement.business_rules,
            ],

        )

        try:

            # --------------------------------------------------
            # Hallucination
            # --------------------------------------------------

            info(
                "Running Hallucination Metric..."
            )

            hallucination = (
                self.hallucination.evaluate(
                    test_case
                )
            )

            success(
                "Hallucination Completed"
            )

            # --------------------------------------------------
            # Correctness
            # --------------------------------------------------

            info(
                "Running Correctness Metric..."
            )

            correctness = (
                self.correctness.evaluate(
                    test_case
                )
            )

            success(
                "Correctness Completed"
            )

            # --------------------------------------------------
            # Answer Relevancy
            # --------------------------------------------------

            info(
                "Running Answer Relevancy Metric..."
            )

            answer_relevancy = (
                self.answer_relevancy.evaluate(
                    test_case
                )
            )

            success(
                "Answer Relevancy Completed"
            )

            # --------------------------------------------------
            # Overall AI Evaluation Score
            # --------------------------------------------------

            overall_score = round(

                (
                    hallucination["score"]
                    + correctness["score"]
                    + answer_relevancy["score"]
                ) / 3,

                2,

            )

            return {

                "validator": "DeepEval",

                "status": "SUCCESS",

                "score": overall_score,

                "hallucination": hallucination,

                "correctness": correctness,

                "answer_relevancy": answer_relevancy,

            }

        except Exception as exception:

            failed(
                f"DeepEval Failed : {exception}"
            )

            return {

                "validator": "DeepEval",

                "status": "FAILED",

                "score": 0,

                "hallucination": {
                    "score": 0,
                    "reason": "",
                },

                "correctness": {
                    "score": 0,
                    "reason": "",
                },

                "answer_relevancy": {
                    "score": 0,
                    "reason": "",
                },

                "error": str(exception),

            }
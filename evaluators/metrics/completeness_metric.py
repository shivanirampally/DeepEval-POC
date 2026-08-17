from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams

from config.settings import COMPLETENESS_THRESHOLD
from config.prompt_templates import COMPLETENESS_CRITERIA


class CompletenessEvaluator:

    def __init__(self, evaluator):

        self.metric = GEval(
            name="Completeness",
            criteria=COMPLETENESS_CRITERIA,
            evaluation_params=[
                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,
            ],
            threshold=COMPLETENESS_THRESHOLD,
            model=evaluator,
        )

    def evaluate(self, test_case):

        self.metric.measure(test_case)

        score = round(
            self.metric.score * 100,
            2,
        )

        return {
            "score": score,
            "gap": round(
                100 - score,
                2,
            ),
            "reason": self.metric.reason,
            "recommendation": (
                "Add test scenarios that are missing from "
                "the benchmark reference."
                if score < 100
                else
                "Benchmark coverage is complete."
            ),
            "passed": score >= (
                COMPLETENESS_THRESHOLD * 100
            ),
        }
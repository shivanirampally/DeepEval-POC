from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams

from config.settings import CORRECTNESS_THRESHOLD
from config.prompt_templates import CORRECTNESS_CRITERIA


class CorrectnessEvaluator:

    def __init__(self, evaluator):

        self.metric = GEval(
            name="Correctness",
            criteria=CORRECTNESS_CRITERIA,
            evaluation_params=[
                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,
            ],
            threshold=CORRECTNESS_THRESHOLD,
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
                "Review generated test cases that differ "
                "from the benchmark or expected behavior."
                if score < 100
                else
                "Generated test cases are correct."
            ),
            "passed": score >= (
                CORRECTNESS_THRESHOLD * 100
            ),
        }
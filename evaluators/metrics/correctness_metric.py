from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams
from config.settings import CORRECTNESS_THRESHOLD
from config.prompt_templates import CORRECTNESS_CRITERIA


class CorrectnessEvaluator:
    def __init__(self, judge):
        self.metric = GEval(
            name="Correctness",
            criteria=CORRECTNESS_CRITERIA,
            evaluation_params=[
                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,
            ],
            threshold=CORRECTNESS_THRESHOLD,
            model=judge,
        )

    def evaluate(self, test_case):
        self.metric.measure(test_case)
        score = round(self.metric.score * 100, 2,)

        return {
            "score": score,
            "reason": self.metric.reason,
            "passed": score >= (CORRECTNESS_THRESHOLD * 100),
        }
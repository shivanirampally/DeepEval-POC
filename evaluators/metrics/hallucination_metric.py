from deepeval.metrics import HallucinationMetric
from config.settings import HALLUCINATION_THRESHOLD


class HallucinationEvaluator:

    def __init__(self, evaluator):

        self.metric = HallucinationMetric(
            threshold=HALLUCINATION_THRESHOLD,
            model=evaluator,
        )

    def evaluate(self, test_case):

        self.metric.measure(test_case)

        risk = round(
            self.metric.score * 100,
            2,
        )

        free = round(
            100 - risk,
            2,
        )

        return {
            "score": free,
            "gap": risk,
            "reason": self.metric.reason,
            "recommendation": (
                "Review generated content for unsupported "
                "functionality or assumptions."
                if risk > 0
                else
                "No hallucination risk detected."
            ),
            "passed": risk <= (
                HALLUCINATION_THRESHOLD * 100
            ),
        }
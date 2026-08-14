from deepeval.metrics import HallucinationMetric
from config.settings import HALLUCINATION_THRESHOLD


class HallucinationEvaluator:
    def __init__(self, judge):
        self.metric = HallucinationMetric(
            threshold=HALLUCINATION_THRESHOLD,
            model=judge,
        )

    def evaluate(self, test_case):
        self.metric.measure(test_case)
        risk = round(self.metric.score * 100, 2,)
        score = round(100 - risk, 2,)
        return {
            "score": score,
            "risk": risk,
            "reason": self.metric.reason,
            "passed": risk <= (HALLUCINATION_THRESHOLD * 100),
        }
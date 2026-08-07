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

        free_score = round(
            self.metric.score * 100,
            2,
        )

        return {

            "score": free_score,

            "risk": round(
                100 - free_score,
                2,
            ),

            "reason": self.metric.reason,

        }
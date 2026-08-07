from deepeval.metrics import FaithfulnessMetric
from config.settings import (FAITHFULNESS_THRESHOLD,)


class FaithfulnessEvaluator:
    """
    Evaluates whether the generated test cases
    remain faithful to the provided requirement
    without introducing unsupported information.
    """

    def __init__(self, judge):
        self.metric = FaithfulnessMetric(
            threshold=FAITHFULNESS_THRESHOLD,
            model=judge,
        )

    # Evaluate
    def evaluate(self, test_case):
        self.metric.measure(test_case)
        score = round(
            self.metric.score * 100,
            2,
        )

        return {
            "score": score,
            "faithfulness_risk": round(
                100 - score,
                2,
            ),

            "reason": self.metric.reason,
            "passed": score >= (
                FAITHFULNESS_THRESHOLD * 100
            ),

        }
from deepeval.metrics import AnswerRelevancyMetric
from config.settings import RELEVANCY_THRESHOLD


class AnswerRelevancyEvaluator:

    def __init__(self, judge):
        self.metric = AnswerRelevancyMetric(
            threshold=RELEVANCY_THRESHOLD,
            model=judge,
        )

    def evaluate(self, test_case):
        self.metric.measure(test_case)
        score = round(self.metric.score * 100, 2,)

        return {
            "score": score,
            "reason": self.metric.reason,
            "passed": score >= (RELEVANCY_THRESHOLD * 100 ),
        }
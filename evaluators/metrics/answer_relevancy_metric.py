from deepeval.metrics import (
    AnswerRelevancyMetric,
)

from config.settings import (
    RELEVANCY_THRESHOLD,
)


class AnswerRelevancyEvaluator:

    def __init__(self, judge):

        self.metric = AnswerRelevancyMetric(

            threshold=RELEVANCY_THRESHOLD,

            model=judge,

        )

    def evaluate(self, test_case):

        self.metric.measure(test_case)

        return {

            "score": round(
                self.metric.score * 100,
                2,
            ),

            "reason": self.metric.reason,

        }
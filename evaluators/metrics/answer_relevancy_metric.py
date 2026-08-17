from deepeval.metrics import AnswerRelevancyMetric

from config.settings import RELEVANCY_THRESHOLD


class AnswerRelevancyEvaluator:

    def __init__(self, evaluator):

        self.metric = AnswerRelevancyMetric(
            threshold=RELEVANCY_THRESHOLD,
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
                "Remove irrelevant or unrelated test "
                "scenarios."
                if score < 100
                else
                "Generated content is relevant."
            ),
            "passed": score >= (
                RELEVANCY_THRESHOLD * 100
            ),
        }
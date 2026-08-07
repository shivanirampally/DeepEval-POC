from deepeval.metrics import ContextualRecallMetric

from config.settings import CONTEXT_RECALL_THRESHOLD


class ContextRecallEvaluator:

    def __init__(self, judge):

        self.metric = ContextualRecallMetric(

            threshold=CONTEXT_RECALL_THRESHOLD,

            model=judge,

        )

    def evaluate(self, test_case):

        self.metric.measure(test_case)

        score = round(self.metric.score*100,2)

        return {

            "score": score,

            "missing_context": round(100-score,2),

            "reason": self.metric.reason,

            "passed": score >= (
                CONTEXT_RECALL_THRESHOLD*100
            ),

        }
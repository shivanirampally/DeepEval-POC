from deepeval.metrics import ContextualPrecisionMetric
from config.settings import CONTEXT_PRECISION_THRESHOLD
from config.prompt_templates import CONTEXT_PRECISION_CRITERIA


class ContextPrecisionEvaluator:

    def __init__(self, judge):

        self.metric = ContextualPrecisionMetric(

            threshold=CONTEXT_PRECISION_THRESHOLD,

            model=judge,

        )

    def evaluate(self, test_case):

        self.metric.measure(test_case)

        score = round(self.metric.score * 100,2)

        return {

            "score": score,

            "irrelevant_context": round(100-score,2),

            "reason": self.metric.reason,

            "passed": score >= (
                CONTEXT_PRECISION_THRESHOLD*100
            ),

        }
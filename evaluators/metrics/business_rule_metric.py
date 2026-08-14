from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams
from config.settings import BUSINESS_RULE_THRESHOLD
from config.prompt_templates import BUSINESS_RULE_CRITERIA


class BusinessRuleEvaluator:

    def __init__(self, judge):
        self.metric = GEval(
            name="Business Rule",
            criteria=BUSINESS_RULE_CRITERIA,
            evaluation_params=[
                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,
            ],
            threshold=BUSINESS_RULE_THRESHOLD,
            model=judge,
        )

    def evaluate(self, test_case):
        self.metric.measure(test_case)
        score = round(self.metric.score * 100, 2, )

        return {
            "score": score,
            "business_rule_risk": round( 100 - score, 2,),
            "reason": self.metric.reason,
            "passed": score >= (BUSINESS_RULE_THRESHOLD * 100),
        }
from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams

from config.settings import REQUIREMENT_THRESHOLD
from config.prompt_templates import REQUIREMENT_CRITERIA


class RequirementEvaluator:

    def __init__(self, evaluator):

        self.metric = GEval(
            name="Requirement Satisfaction",
            criteria=REQUIREMENT_CRITERIA,
            evaluation_params=[
                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,
            ],
            threshold=REQUIREMENT_THRESHOLD,
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
                "Review test cases that do not fully "
                "satisfy the requirement."
                if score < 100
                else
                "Requirement is fully satisfied."
            ),
            "passed": score >= (
                REQUIREMENT_THRESHOLD * 100
            ),
        }
from deepeval.metrics import GEval

from deepeval.test_case import SingleTurnParams

from config.prompt_templates import REQUIREMENT_CRITERIA


class RequirementEvaluator:

    def __init__(self,judge):

        self.metric=GEval(

            name="Requirement Satisfaction",

            criteria=REQUIREMENT_CRITERIA,

            evaluation_params=[

                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,

            ],

            model=judge,

        )

    def evaluate(self,test_case):

        self.metric.measure(test_case)

        score=round(self.metric.score*100,2)

        return{

            "score":score,

            "unsatisfied_requirement":round(100-score,2),

            "reason":self.metric.reason,

            "passed":score>=90,

        }
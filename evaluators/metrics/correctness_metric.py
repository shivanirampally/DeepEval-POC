from deepeval.metrics import GEval

from deepeval.test_case import (
    SingleTurnParams,
)

from config.prompt_templates import (
    CORRECTNESS_CRITERIA,
)


class CorrectnessEvaluator:

    def __init__(self, judge):

        self.metric = GEval(

            name="Correctness",

            criteria=CORRECTNESS_CRITERIA,

            evaluation_params=[

                SingleTurnParams.INPUT,

                SingleTurnParams.ACTUAL_OUTPUT,

                SingleTurnParams.EXPECTED_OUTPUT,

            ],

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
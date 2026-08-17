from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams


class RequirementQualityEvaluator:
    """
    Evaluates generated test cases against the requirement itself.

    IMPORTANT:
        This evaluator does NOT use benchmark test cases.

    Purpose:
        Determine whether the generated test cases are:
            - relevant to the requirement
            - logically structured
            - actionable
            - free from unsupported functionality
            - reasonably comprehensive
    """

    THRESHOLD = 90

    def __init__(self, evaluator):

        self.metric = GEval(
            name="Requirement Alignment",

            criteria="""
Evaluate the quality of the generated test cases based ONLY on the
provided requirement.

Do NOT compare the generated test cases with a benchmark repository,
ground-truth test cases, expected test cases, or reference scenarios.

Evaluate the following:

1. Requirement relevance
   - Every generated test case should relate directly to the requirement.

2. Requirement alignment
   - Test cases should validate functionality explicitly described by
     the requirement.

3. Logical test flow
   - Test steps should be logically ordered and actionable.

4. Expected result quality
   - Expected results should logically follow from the test steps.

5. Unsupported assumptions
   - The generated test cases should not introduce functionality,
     rules, screens, validations, or behavior that are not supported
     by the requirement.

6. Test design quality
   - Where applicable, the generated suite should contain meaningful
     positive, negative, boundary, and edge scenarios.

7. Business usefulness
   - The generated test cases should be understandable and useful
     for QA and business stakeholders.

Give a score based only on the requirement and generated output.
""",

            evaluation_params=[
                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
            ],

            threshold=self.THRESHOLD / 100,

            model=evaluator,
        )

    def evaluate(self, test_case):

        self.metric.measure(test_case)

        score = round(
            self.metric.score * 100,
            2,
        )

        gap = round(
            100 - score,
            2,
        )

        return {
            "score": score,
            "gap": gap,
            "reason": self.metric.reason,
            "recommendation": (
                self._get_recommendation(score)
            ),
            "passed": score >= self.THRESHOLD,
        }

    @staticmethod
    def _get_recommendation(score):

        if score >= 90:
            return (
                "Generated test cases are well aligned "
                "with the requirement."
            )

        if score >= 75:
            return (
                "Review test cases for requirement alignment, "
                "logical test flow, expected results, and "
                "unsupported assumptions."
            )

        return (
            "Generated test cases require significant review. "
            "Check requirement alignment, unsupported behavior, "
            "test flow, and missing meaningful scenarios."
        )
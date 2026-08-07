from evaluators.framework.schema_validator import SchemaValidator
from evaluators.framework.testcase_validator import TestCaseValidator
from evaluators.framework.coverage_validator import CoverageValidator
from evaluators.deepeval_metrics import DeepEvalMetrics
from evaluators.scoring.score_calculator import ScoreCalculator
from evaluators.results.evaluation_result import EvaluationResult


class LLMEvaluator:

    def __init__(self):

        self.schema_validator = SchemaValidator()

        self.testcase_validator = TestCaseValidator()

        self.coverage_validator = CoverageValidator()

        self.deepeval = DeepEvalMetrics()

    # ---------------------------------------------------------
    # Evaluate
    # ---------------------------------------------------------

    def evaluate(
        self,
        *,
        generator,
        requirement,
        generated_json,
    ):

        # -----------------------------------------
        # Schema Validation
        # -----------------------------------------

        schema_result = self.schema_validator.validate(
            generated_json
        )

        if schema_result["status"] == "FAILED":

            return schema_result

        parsed_json = schema_result["data"]

        # -----------------------------------------
        # Test Case Validation
        # -----------------------------------------

        testcase_result = self.testcase_validator.validate(
            parsed_json
        )

        # -----------------------------------------
        # Coverage Validation
        # -----------------------------------------

        coverage_result = self.coverage_validator.validate(
            requirement,
            parsed_json,
        )

        # -----------------------------------------
        # DeepEval
        # -----------------------------------------

        deepeval_result = self.deepeval.evaluate(

            requirement=requirement,

            generated_json=parsed_json,

        )

        # -----------------------------------------
        # Overall Score
        # -----------------------------------------

        score = ScoreCalculator.calculate(

            schema_result,

            testcase_result,

            coverage_result,

            deepeval_result,

        )

        # -----------------------------------------
        # Final Result
        # -----------------------------------------

        return EvaluationResult.build(

            generator=generator,

            requirement=requirement,

            generated_json=parsed_json,

            schema=schema_result,

            testcase=testcase_result,

            coverage=coverage_result,

            deepeval=deepeval_result,

            score=score,

        )
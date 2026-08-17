from evaluators.framework.schema_validator import SchemaValidator
from evaluators.framework.testcase_validator import TestCaseValidator
from evaluators.framework.coverage_validator import CoverageValidator

from evaluators.deepeval_metrics import DeepEvalMetrics

from evaluators.scoring.score_calculator import ScoreCalculator
from evaluators.results.evaluation_result import EvaluationResult

from utils.logger import (
    info,
    success,
    failed,
)


class LLMEvaluator:
    """
    Main evaluation orchestrator.

    Flow:

    Generated Output
        ↓
    Schema Validation
        ↓
    Test Case Quality Validation
        ↓
    Coverage Validation
        ↓
    Benchmark DeepEval
        ↓
    Requirement-Only DeepEval
        ↓
    Score Calculation
        ↓
    Standardized EvaluationResult
    """

    def __init__(self):

        self.schema_validator = SchemaValidator()

        self.testcase_validator = (
            TestCaseValidator()
        )

        self.coverage_validator = (
            CoverageValidator()
        )

        self.deepeval = (
            DeepEvalMetrics()
        )

    # ==========================================================
    # EVALUATE
    # ==========================================================

    def evaluate(
        self,
        *,
        generator,
        requirement,
        generated_output,
        evaluation_output,
    ):

        try:

            # ==================================================
            # 1. Schema Validation
            # ==================================================

            info(
                "Running Schema validation..."
            )

            schema_result = (
                self.schema_validator.validate(
                    generated_output
                )
            )

            if schema_result["status"] == "FAILED":

                failed(
                    "Schema Validation Failed"
                )

                return EvaluationResult.build(
                    generator=generator,
                    requirement=requirement,
                    generated_output=generated_output,
                    evaluation_output=evaluation_output,

                    schema=schema_result,

                    testcase={
                        "validator": "TestCaseValidator",
                        "status": "NOT_EXECUTED",
                        "score": 0,
                        "errors": [
                            "Skipped because schema validation failed."
                        ],
                        "warnings": [],
                        "statistics": {},
                    },

                    coverage={
                        "validator": "CoverageValidator",
                        "status": "NOT_EXECUTED",
                        "score": 0,
                        "errors": [
                            "Skipped because schema validation failed."
                        ],
                        "warnings": [],
                        "statistics": {},
                    },

                    deepeval_evaluation={
                        "validator": "DeepEval",
                        "status": "NOT_EXECUTED",
                        "score": 0,
                        "error": (
                            "Skipped because schema validation failed."
                        ),
                    },

                    requirement_only_evaluation={
                        "validator": (
                            "DeepEval Requirement-Only"
                        ),
                        "status": "NOT_EXECUTED",
                        "score": 0,
                        "error": (
                            "Skipped because schema validation failed."
                        ),
                    },

                    score={
                        "quality_validation_score": 0,
                        "deepeval_evaluation_score": 0,
                        "overall_score": 0,
                        "status": "FAIL",
                        "execution_time": 0,
                        "winner": "",
                    },
                )

            success(
                "Schema Validation Passed"
            )

            parsed_output = (
                schema_result["data"]
            )

            # ==================================================
            # 2. Test Case Quality
            # ==================================================

            info(
                "Running Test Case Quality Validation..."
            )

            testcase_result = (
                self.testcase_validator.validate(
                    parsed_output
                )
            )

            success(
                "Test Case Quality Validation Passed"
            )

            # ==================================================
            # 3. Coverage
            # ==================================================

            info(
                "Running Coverage Validation..."
            )

            coverage_result = (
                self.coverage_validator.validate(
                    requirement,
                    parsed_output,
                )
            )

            success(
                "Coverage Validation Passed"
            )

            # ==================================================
            # 4. Benchmark DeepEval
            # ==================================================

            info(
                "Running Benchmark DeepEval Evaluation..."
            )

            deepeval_result = (
                self.deepeval.evaluate(
                    requirement=requirement,
                    generated_output=parsed_output,
                    evaluation_output=evaluation_output,
                )
            )

            success(
                "Benchmark DeepEval Evaluation Completed"
            )

            # ==================================================
            # 5. Requirement-Only DeepEval
            # ==================================================

            info(
                "Running Requirement-Only Evaluation..."
            )

            requirement_only_result = (
                self.deepeval.evaluate_requirement_only(
                    requirement=requirement,
                    generated_output=parsed_output,
                )
            )

            success(
                "Requirement-Only Evaluation Completed"
            )

            # ==================================================
            # 6. Overall Score
            # ==================================================

            info(
                "Calculating Overall Score..."
            )

            score = (
                ScoreCalculator.calculate(
                    schema_result,
                    testcase_result,
                    coverage_result,
                    deepeval_result,
                )
            )

            success(
                "Overall Score Calculated"
            )

            # ==================================================
            # 7. Standardized Result
            # ==================================================

            result = (
                EvaluationResult.build(
                    generator=generator,
                    requirement=requirement,
                    generated_output=parsed_output,
                    evaluation_output=evaluation_output,

                    schema=schema_result,
                    testcase=testcase_result,
                    coverage=coverage_result,

                    deepeval_evaluation=(
                        deepeval_result
                    ),

                    requirement_only_evaluation=(
                        requirement_only_result
                    ),

                    score=score,
                )
            )

            success(
                "Evaluation Result Ready"
            )

            return result

        except Exception as exception:

            failed(
                f"Evaluation Engine Failed : "
                f"{exception}"
            )

            return EvaluationResult.build(
                generator=generator,
                requirement=requirement,
                generated_output=generated_output,
                evaluation_output=evaluation_output,

                schema={
                    "validator": "SchemaValidator",
                    "status": "FAILED",
                    "score": 0,
                    "errors": [str(exception)],
                    "warnings": [],
                    "statistics": {},
                },

                testcase={
                    "validator": "TestCaseValidator",
                    "status": "FAILED",
                    "score": 0,
                    "errors": [],
                    "warnings": [],
                    "statistics": {},
                },

                coverage={
                    "validator": "CoverageValidator",
                    "status": "FAILED",
                    "score": 0,
                    "errors": [],
                    "warnings": [],
                    "statistics": {},
                },

                deepeval_evaluation={
                    "validator": "DeepEval",
                    "status": "FAILED",
                    "score": 0,
                    "error": str(exception),
                },

                requirement_only_evaluation={
                    "validator": (
                        "DeepEval Requirement-Only"
                    ),
                    "status": "FAILED",
                    "score": 0,
                    "error": str(exception),
                },

                score={
                    "quality_validation_score": 0,
                    "deepeval_evaluation_score": 0,
                    "overall_score": 0,
                    "status": "FAIL",
                    "execution_time": 0,
                    "winner": "",
                },
            )
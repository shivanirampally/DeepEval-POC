import json

from deepeval.test_case import LLMTestCase

from config.judge_settings import OllamaJudge
from config.settings import JUDGE_MODEL

from evaluators.metrics.hallucination_metric import (
    HallucinationEvaluator,
)

from evaluators.metrics.correctness_metric import (
    CorrectnessEvaluator,
)

from evaluators.metrics.completeness_metric import (
    CompletenessEvaluator,
)

from evaluators.metrics.business_rule_metric import (
    BusinessRuleEvaluator,
)

from evaluators.metrics.requirement_metric import (
    RequirementEvaluator,
)

from evaluators.metrics.answer_relevancy_metric import (
    AnswerRelevancyEvaluator,
)

from utils.logger import (
    info,
    success,
    failed,
)


class DeepEvalMetrics:
    """
    Runs DeepEval metrics against QA Boat generated
    test cases.

    DeepEval receives:

        actual_output
            -> Raw QA Boat generated test cases

        expected_output
            -> Benchmark/reference test cases

        context
            -> Requirement and business context

    The benchmark reference is built from the
    EvaluationJsonBuilder output so that DeepEval
    works with dictionaries rather than BenchmarkTestCase
    model objects.
    """

    def __init__(self):

        evaluator = OllamaJudge()

        self.hallucination = HallucinationEvaluator(
            evaluator
        )

        self.correctness = CorrectnessEvaluator(
            evaluator
        )

        self.completeness = CompletenessEvaluator(
            evaluator
        )

        self.business_rule = BusinessRuleEvaluator(
            evaluator
        )

        self.requirement = RequirementEvaluator(
            evaluator
        )

        self.answer_relevancy = (
            AnswerRelevancyEvaluator(
                evaluator
            )
        )

    # ==========================================================
    # EVALUATE
    # ==========================================================

    def evaluate(
        self,
        *,
        requirement,
        generated_output,
        evaluation_output,
    ):

        try:

            # ==================================================
            # Actual QA Boat Output
            # ==================================================

            actual_output = json.dumps(
                generated_output,
                indent=2,
                ensure_ascii=False,
            )

            # ==================================================
            # Benchmark Reference
            # ==================================================

            benchmark_output = (
                self._build_benchmark_reference(
                    evaluation_output
                )
            )

            # ==================================================
            # Debug Information
            # ==================================================

            info(
                "Preparing DeepEval test case..."
            )

            info(
                f"Generated test cases : "
                f"{len(generated_output.get('testCases', []))}"
            )

            info(
                f"Benchmark reference size : "
                f"{len(benchmark_output)} characters"
            )

            # ==================================================
            # DeepEval Test Case
            # ==================================================

            test_case = LLMTestCase(

                input=requirement.description,

                actual_output=actual_output,

                expected_output=benchmark_output,

                context=[
                    requirement.description,
                    requirement.business_rules or "",
                    benchmark_output,
                ],
            )

            # ==================================================
            # Hallucination
            # ==================================================

            info(
                "Running Hallucination Metric..."
            )

            hallucination = (
                self.hallucination.evaluate(
                    test_case
                )
            )

            success(
                "Hallucination Completed"
            )

            # ==================================================
            # Correctness
            # ==================================================

            info(
                "Running Correctness Metric..."
            )

            correctness = (
                self.correctness.evaluate(
                    test_case
                )
            )

            success(
                "Correctness Completed"
            )

            # ==================================================
            # Completeness
            # ==================================================

            info(
                "Running Completeness Metric..."
            )

            completeness = (
                self.completeness.evaluate(
                    test_case
                )
            )

            success(
                "Completeness Completed"
            )

            # ==================================================
            # Business Rule
            # ==================================================

            info(
                "Running Business Rule Metric..."
            )

            business_rule = (
                self.business_rule.evaluate(
                    test_case
                )
            )

            success(
                "Business Rule Completed"
            )

            # ==================================================
            # Requirement
            # ==================================================

            info(
                "Running Requirement Metric..."
            )

            requirement_result = (
                self.requirement.evaluate(
                    test_case
                )
            )

            success(
                "Requirement Completed"
            )

            # ==================================================
            # Answer Relevancy
            # ==================================================

            info(
                "Running Answer Relevancy Metric..."
            )

            answer_relevancy = (
                self.answer_relevancy.evaluate(
                    test_case
                )
            )

            success(
                "Answer Relevancy Completed"
            )

            # ==================================================
            # DeepEval Overall Score
            # ==================================================

            deepeval_score = round(
                (
                    hallucination["score"]
                    + correctness["score"]
                    + completeness["score"]
                    + business_rule["score"]
                    + requirement_result["score"]
                    + answer_relevancy["score"]
                ) / 6,
                2,
            )

            # ==================================================
            # Result
            # ==================================================

            return {

                "validator": "DeepEval",

                "status": "SUCCESS",

                "score": deepeval_score,

                "hallucination": hallucination,

                "correctness": correctness,

                "completeness": completeness,

                "business_rule": business_rule,

                "requirement": requirement_result,

                "answer_relevancy": answer_relevancy,

                "evaluator_model": JUDGE_MODEL,
            }

        except Exception as exception:

            failed(
                f"DeepEval Evaluation Failed : "
                f"{exception}"
            )

            raise

    # ==========================================================
    # BUILD BENCHMARK REFERENCE
    # ==========================================================

    @staticmethod
    def _build_benchmark_reference(
        evaluation_output,
    ) -> str:

        sections = []

        header = evaluation_output.get(
            "header",
            {},
        )

        # ======================================================
        # Requirement
        # ======================================================

        sections.append(
            "=== REQUIREMENT REFERENCE ===\n"
            f"Requirement ID: "
            f"{header.get('requirementId', '')}\n"
            f"Requirement Type: "
            f"{header.get('requirementType', '')}\n"
            f"Title: "
            f"{header.get('title', '')}\n"
            f"Description: "
            f"{header.get('description', '')}\n"
            f"Business Rules: "
            f"{header.get('businessRules', '')}\n"
            f"Priority: "
            f"{header.get('priority', '')}"
        )

        # ======================================================
        # User Story Benchmark Scenarios
        # ======================================================

        user_story_scenarios = header.get(
            "userStoryScenarios",
            [],
        )

        if user_story_scenarios:

            sections.append(
                "=== USER STORY BENCHMARK SCENARIOS ==="
            )

            for scenario in user_story_scenarios:

                sections.append(
                    DeepEvalMetrics
                    ._format_user_story_scenario(
                        scenario
                    )
                )

        # ======================================================
        # Acceptance Criteria
        # ======================================================

        acceptance_criteria = header.get(
            "acceptanceCriteria",
            [],
        )

        if acceptance_criteria:

            sections.append(
                "=== ACCEPTANCE CRITERIA ==="
            )

            for acceptance_criterion in (
                acceptance_criteria
            ):

                sections.append(
                    DeepEvalMetrics
                    ._format_acceptance_criteria(
                        acceptance_criterion
                    )
                )

        return "\n\n".join(
            sections
        )

    # ==========================================================
    # USER STORY FORMAT
    # ==========================================================

    @staticmethod
    def _format_user_story_scenario(
        scenario,
    ) -> str:

        steps = scenario.get(
            "steps",
            [],
        )

        return (
            f"Benchmark ID: "
            f"{scenario.get('benchmarkTestCaseId', '')}\n"
            f"Requirement ID: "
            f"{scenario.get('requirementId', '')}\n"
            f"Scenario: "
            f"{scenario.get('scenario', '')}\n"
            f"Category: "
            f"{scenario.get('category', '')}\n"
            f"Priority: "
            f"{scenario.get('priority', '')}\n"
            f"Precondition: "
            f"{scenario.get('precondition', '')}\n"
            f"Test Data: "
            f"{scenario.get('testData', '')}\n"
            f"Steps:\n"
            f"{DeepEvalMetrics._format_steps(steps)}\n"
            f"Expected Result: "
            f"{scenario.get('expectedResult', '')}"
        )

    # ==========================================================
    # ACCEPTANCE CRITERIA FORMAT
    # ==========================================================

    @staticmethod
    def _format_acceptance_criteria(
        acceptance_criterion,
    ) -> str:

        sections = []

        sections.append(
            f"Acceptance Criteria ID: "
            f"{acceptance_criterion.get('id', '')}\n"
            f"Title: "
            f"{acceptance_criterion.get('title', '')}\n"
            f"Description: "
            f"{acceptance_criterion.get('description', '')}\n"
            f"Priority: "
            f"{acceptance_criterion.get('priority', '')}"
        )

        benchmark_testcases = (
            acceptance_criterion.get(
                "benchmarkTestCases",
                [],
            )
        )

        if benchmark_testcases:

            sections.append(
                "Benchmark Test Cases:"
            )

            for testcase in benchmark_testcases:

                sections.append(
                    DeepEvalMetrics
                    ._format_benchmark_testcase(
                        testcase
                    )
                )

        return "\n".join(
            sections
        )

    # ==========================================================
    # BENCHMARK TEST CASE FORMAT
    # ==========================================================

    @staticmethod
    def _format_benchmark_testcase(
        testcase,
    ) -> str:

        steps = testcase.get(
            "steps",
            [],
        )

        return (
            f"Test Case ID: "
            f"{testcase.get('id', '')}\n"
            f"Acceptance Criteria Ref: "
            f"{testcase.get('acceptanceCriteriaRef', '')}\n"
            f"Test Type: "
            f"{testcase.get('testType', '')}\n"
            f"Technique: "
            f"{testcase.get('technique', '')}\n"
            f"Priority: "
            f"{testcase.get('priority', '')}\n"
            f"Description: "
            f"{testcase.get('description', '')}\n"
            f"Precondition: "
            f"{testcase.get('precondition', '')}\n"
            f"Test Data: "
            f"{testcase.get('testData', '')}\n"
            f"Steps:\n"
            f"{DeepEvalMetrics._format_steps(steps)}\n"
            f"Expected Result: "
            f"{testcase.get('expectedResult', '')}\n"
            f"DeepEval Reference: "
            f"{testcase.get('deepEvalReference', '')}"
        )

    # ==========================================================
    # STEPS
    # ==========================================================

    @staticmethod
    def _format_steps(
        steps,
    ) -> str:

        if not steps:
            return ""

        return "\n".join(
            str(step)
            for step in steps
        )
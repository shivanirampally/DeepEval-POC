from models.requirement import Requirement


class EvaluationJsonBuilder:
    """
    Builds the evaluation JSON from:

        Requirement repository
                +
        Raw QA Boat(Qwen3) generated JSON

    IMPORTANT
    ---------
    This class does NOT modify the original QA Boat output.

    The raw Qwen3 response remains:

    {
        "testCases": [
            {
                "testCaseId": "...",
                "testDescription": "...",
                "testSteps": [],
                "expectedResult": "..."
            }
        ]
    }

    This builder creates a separate evaluation representation.
    """

    @staticmethod
    def build(
        *,
        requirement: Requirement,
        generated_output: dict,
    ) -> dict:

        # ==================================================
        # HEADER
        # ==================================================

        header = {
            "requirementId": requirement.requirement_id,
            "requirementType": requirement.requirement_type,
            "title": requirement.title,
            "description": requirement.description,
            "businessRules": requirement.business_rules,
            "priority": requirement.priority,

            # --------------------------------------------------
            # User Story Benchmark Scenarios
            # --------------------------------------------------

            "userStoryScenarios": (
                EvaluationJsonBuilder
                ._build_user_story_scenarios(
                    requirement
                )
            ),

            # --------------------------------------------------
            # Acceptance Criteria
            # --------------------------------------------------

            "acceptanceCriteria": (
                EvaluationJsonBuilder
                ._build_acceptance_criteria(
                    requirement
                )
            ),
        }

        # ==================================================
        # BODY
        # ==================================================

        body = {
            "testCases": generated_output.get(
                "testCases",
                [],
            )
        }

        # ==================================================
        # FINAL EVALUATION JSON
        # ==================================================

        return {
            "header": header,
            "body": body,
        }

    # ======================================================
    # USER STORY BENCHMARKS
    # ======================================================

    @staticmethod
    def _build_user_story_scenarios(
        requirement: Requirement,
    ) -> list:

        scenarios = []

        for benchmark in (
            requirement.user_story_benchmarks
            or []
        ):

            scenarios.append(
                {
                    "benchmarkTestCaseId": (
                        benchmark.benchmark_test_case_id
                    ),

                    "requirementId": (
                        benchmark.requirement_id
                    ),

                    "scenario": (
                        benchmark.scenario
                    ),

                    "category": (
                        benchmark.category
                    ),

                    "priority": (
                        benchmark.priority
                    ),

                    "precondition": (
                        benchmark.precondition
                    ),

                    "testData": (
                        benchmark.test_data
                    ),

                    "steps": (
                        benchmark.steps
                    ),

                    "expectedResult": (
                        benchmark.expected_result
                    ),

                    "source": (
                        benchmark.source
                    ),

                    "deepEvalReference": (
                        benchmark.deep_eval_reference
                    ),
                }
            )

        return scenarios

    # ======================================================
    # ACCEPTANCE CRITERIA
    # ======================================================

    @staticmethod
    def _build_acceptance_criteria(
        requirement: Requirement,
    ) -> list:

        acceptance_criteria = []

        for ac in (
            requirement.acceptance_criteria
            or []
        ):

            benchmark_testcases = []

            for testcase in (
                ac.benchmark_testcases
                or []
            ):

                benchmark_testcases.append(
                    {
                        "id": (
                            testcase.test_case_id
                        ),

                        "acceptanceCriteriaRef": (
                            testcase.acceptance_criteria_ref
                        ),

                        "testType": (
                            testcase.test_type
                        ),

                        "technique": (
                            testcase.technique
                        ),

                        "priority": (
                            testcase.priority
                        ),

                        "description": (
                            testcase.description
                        ),

                        "precondition": (
                            testcase.precondition
                        ),

                        "testData": (
                            testcase.test_data
                        ),

                        "steps": (
                            testcase.steps
                        ),

                        "expectedResult": (
                            testcase.expected_result
                        ),

                        "deepEvalReference": (
                            getattr(
                                testcase,
                                "deep_eval_reference",
                                "",
                            )
                        ),
                    }
                )

            acceptance_criteria.append(
                {
                    "id": (
                        ac.acceptance_criteria_id
                    ),

                    "title": (
                        ac.title
                    ),

                    "description": (
                        ac.description
                    ),

                    "priority": (
                        ac.priority
                    ),

                    "benchmarkTestCases": (
                        benchmark_testcases
                    ),
                }
            )

        return acceptance_criteria
class EvaluationResult:
    """
    Builds the standardized evaluation result returned by the
    evaluation engine.

    The result keeps three things separate:

        1. Generated QA Boat output
        2. Benchmark repository
           - User Story benchmark scenarios
           - Acceptance Criteria benchmark test cases
        3. Validation / DeepEval results

    BenchmarkTestCase objects are serialized into dictionaries
    only inside the benchmark repository section.
    """

    @staticmethod
    def build(
        *,
        generator,
        requirement,
        generated_output,
        evaluation_output,
        schema,
        testcase,
        coverage,
        deepeval_evaluation,
        requirement_only_evaluation=None,   
        score,
    ):

        # ==========================================================
        # User Story Benchmarks
        # ==========================================================

        user_story_benchmarks = []

        for benchmark in getattr(
            requirement,
            "user_story_benchmarks",
            [],
        ):

            user_story_benchmarks.append(
                {
                    "benchmark_test_case_id": getattr(
                        benchmark,
                        "benchmark_test_case_id",
                        "",
                    ),

                    "requirement_id": getattr(
                        benchmark,
                        "requirement_id",
                        "",
                    ),

                    "scenario": getattr(
                        benchmark,
                        "scenario",
                        "",
                    ),

                    "category": getattr(
                        benchmark,
                        "category",
                        "",
                    ),

                    "priority": getattr(
                        benchmark,
                        "priority",
                        "",
                    ),

                    "precondition": getattr(
                        benchmark,
                        "precondition",
                        "",
                    ),

                    "test_data": getattr(
                        benchmark,
                        "test_data",
                        "",
                    ),

                    "steps": getattr(
                        benchmark,
                        "steps",
                        [],
                    ),

                    "expected_result": getattr(
                        benchmark,
                        "expected_result",
                        "",
                    ),

                    "source": getattr(
                        benchmark,
                        "source",
                        "",
                    ),

                    "deep_eval_reference": getattr(
                        benchmark,
                        "deep_eval_reference",
                        "",
                    ),
                }
            )

        # ==========================================================
        # Acceptance Criteria Benchmarks
        # ==========================================================

        acceptance_criteria_benchmarks = []

        for acceptance_criterion in getattr(
            requirement,
            "acceptance_criteria",
            [],
        ):

            acceptance_criteria_id = getattr(
                acceptance_criterion,
                "acceptance_criteria_id",
                "",
            )

            acceptance_criteria_title = getattr(
                acceptance_criterion,
                "title",
                "",
            )

            acceptance_criteria_description = getattr(
                acceptance_criterion,
                "description",
                "",
            )

            acceptance_criteria_business_rules = getattr(
                acceptance_criterion,
                "business_rules",
                "",
            )

            acceptance_criteria_priority = getattr(
                acceptance_criterion,
                "priority",
                "",
            )

            benchmark_testcases = []

            for benchmark_testcase in getattr(
                acceptance_criterion,
                "benchmark_testcases",
                [],
            ):

                benchmark_testcases.append(
                    {
                        "test_case_id": getattr(
                            benchmark_testcase,
                            "test_case_id",
                            "",
                        ),

                        "acceptance_criteria_ref": getattr(
                            benchmark_testcase,
                            "acceptance_criteria_ref",
                            "",
                        ),

                        "test_type": getattr(
                            benchmark_testcase,
                            "test_type",
                            "",
                        ),

                        "technique": getattr(
                            benchmark_testcase,
                            "technique",
                            "",
                        ),

                        "priority": getattr(
                            benchmark_testcase,
                            "priority",
                            "",
                        ),

                        "description": getattr(
                            benchmark_testcase,
                            "description",
                            "",
                        ),

                        "precondition": getattr(
                            benchmark_testcase,
                            "precondition",
                            "",
                        ),

                        "test_data": getattr(
                            benchmark_testcase,
                            "test_data",
                            "",
                        ),

                        "steps": getattr(
                            benchmark_testcase,
                            "steps",
                            [],
                        ),

                        "expected_result": getattr(
                            benchmark_testcase,
                            "expected_result",
                            "",
                        ),

                        "deep_eval_reference": getattr(
                            benchmark_testcase,
                            "deep_eval_reference",
                            "",
                        ),
                    }
                )

            acceptance_criteria_benchmarks.append(
                {
                    "acceptance_criteria_id": (
                        acceptance_criteria_id
                    ),

                    "title": (
                        acceptance_criteria_title
                    ),

                    "description": (
                        acceptance_criteria_description
                    ),

                    "business_rules": (
                        acceptance_criteria_business_rules
                    ),

                    "priority": (
                        acceptance_criteria_priority
                    ),

                    "benchmark_testcases": (
                        benchmark_testcases
                    ),
                }
            )

        # ==========================================================
        # Additional Benchmark Repositories
        # ==========================================================

        input_variations = getattr(
            requirement,
            "input_variations",
            [],
        )

        usability_navigation = getattr(
            requirement,
            "usability_navigation",
            [],
        )

        non_functional = getattr(
            requirement,
            "non_functional",
            [],
        )

        # ==========================================================
        # Standardized Result
        # ==========================================================

        return {

            # ======================================================
            # Generator
            # ======================================================

            "generator": generator,

            # ======================================================
            # Requirement
            # ======================================================

            "requirement": {

                "id": requirement.requirement_id,

                "type": requirement.requirement_type,

                "title": requirement.title,

                "description": requirement.description,

                "business_rules": (
                    requirement.business_rules
                ),

                "priority": requirement.priority,

            },

            # ======================================================
            # Raw Generated QA Boat Output
            # ======================================================

            "generated_output": generated_output,

            # ======================================================
            # Evaluation JSON
            # ======================================================

            "evaluation_json": evaluation_output,

            # ======================================================
            # Benchmark Repository
            # ======================================================

            "benchmark_repository": {

                "user_story_benchmarks": (
                    user_story_benchmarks
                ),

                "acceptance_criteria_benchmarks": (
                    acceptance_criteria_benchmarks
                ),

                "input_variations": (
                    input_variations
                ),

                "usability_navigation": (
                    usability_navigation
                ),

                "non_functional": (
                    non_functional
                ),

            },

            # ======================================================
            # Framework Validation
            # ======================================================

            "testcase_quality_validation": {

                "schema": schema,

                "testcase": testcase,

                "coverage": coverage,

            },

            # ======================================================
            # DeepEval
            # ======================================================

            "deepeval_evaluation": deepeval_evaluation,
            "requirement_only_evaluation": (
                requirement_only_evaluation
            ),
            # ======================================================
            # Overall Score
            # ======================================================

            "overall": score,

        }
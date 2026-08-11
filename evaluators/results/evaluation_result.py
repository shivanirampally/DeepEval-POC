class EvaluationResult:
    """
    Builds the standardized evaluation result returned by the
    evaluation engine.

    This structure is considered the project contract.
    """

    @staticmethod
    def build(
        *,
        generator,
        requirement,
        generated_output,
        schema,
        testcase,
        coverage,
        deepeval,
        score,
    ):

        return {
            # Generator Information
            "generator": generator,

            # Requirement Information
            "requirement": {
                "id": requirement.requirement_id,
                "type": requirement.requirement_type,
                "title": requirement.title,
                "description": requirement.description,
                "business_rules": requirement.business_rules,
                "priority": requirement.priority,
            },

            # Generated Output
            "generated_output": generated_output,

            # Benchmark Repository
            "benchmark_repository": requirement.benchmark_repository,

            # Framework Validation
            "testcase_quality_validation": {
                "schema": schema,
                "testcase": testcase,
                "coverage": coverage,
            },

            # DeepEval Evaluation
            "ai_evaluation": deepeval,

            # Final Score
            "overall": score,

        }
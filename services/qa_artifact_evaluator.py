from evaluators.deepeval_metrics import DeepEvalMetrics


class QAArtifactEvaluator:
    """
    Evaluates critical QA artifacts produced by the
    QA Boat 21-phase generation workflow.

    Critical artifacts:
        P01 - Story Expansion
        P03 - Task Breakdown
        P09 - Test Case Generation

    Responsibilities:
        - Evaluate Story Expansion at requirement level.
        - Evaluate Task Breakdown at requirement level.
        - Evaluate generated test cases against approved benchmarks.
        - Reuse the existing DeepEvalMetrics implementation.

    This class does NOT:
        - execute QA Boat prompts
        - modify generated artifacts
        - repair generated artifacts
        - remove duplicates
        - calculate final weighted scores
    """

    def __init__(self):
        self.deepeval = DeepEvalMetrics()

    # ==========================================================
    # STORY EXPANSION
    # ==========================================================

    def evaluate_story_expansion(
        self,
        *,
        requirement,
        generated_output: dict,
    ) -> dict:
        """
        Evaluate the Story Expansion artifact.

        This is a requirement-level artifact, so it uses
        the existing requirement-only DeepEval path.
        """

        requirement_text = (
            self._build_requirement_text(
                requirement
            )
        )

        generated_text = (
            self._to_text(
                generated_output
            )
        )

        return self.deepeval.evaluate_requirement_only(
            requirement=requirement_text,
            generated_output=generated_text,
        )

    # ==========================================================
    # TASK BREAKDOWN
    # ==========================================================

    def evaluate_task_breakdown(
        self,
        *,
        requirement,
        expanded_story: dict | str,
        generated_output: dict,
    ) -> dict:
        """
        Evaluate the Task Breakdown artifact.

        The original requirement and expanded story are
        provided as evaluation context.
        """

        requirement_text = (
            self._build_requirement_text(
                requirement
            )
        )

        expanded_story_text = (
            self._to_text(
                expanded_story
            )
        )

        generated_text = (
            self._to_text(
                generated_output
            )
        )

        evaluation_context = (
            "ORIGINAL REQUIREMENT\n"
            f"{requirement_text}\n\n"
            "EXPANDED STORY\n"
            f"{expanded_story_text}"
        )

        return self.deepeval.evaluate_requirement_only(
            requirement=evaluation_context,
            generated_output=generated_text,
        )

    # ==========================================================
    # TEST CASE GENERATION
    # ==========================================================

    def evaluate_test_case_generation(
        self,
        *,
        requirement,
        generated_output: dict,
    ) -> dict:
        """
        Evaluate generated test cases against the approved
        benchmark test cases.

        This uses the existing full benchmark evaluation path.
        """

        evaluation_output = {
            "testCases": (
                generated_output.get(
                    "testCases",
                    [],
                )
            )
        }

        return self.deepeval.evaluate(
            requirement=requirement,
            generated_output=generated_output,
            evaluation_output=evaluation_output,
        )

    # ==========================================================
    # CRITICAL ARTIFACTS
    # ==========================================================

    def evaluate_critical_artifacts(
        self,
        *,
        requirement,
        story_expansion: dict,
        task_breakdown: dict,
        test_case_generation: dict,
    ) -> dict:
        """
        Evaluate the three critical QA Boat artifacts.

        P01 -> Story Expansion
        P03 -> Task Breakdown
        P09 -> Test Case Generation
        """

        story_result = (
            self.evaluate_story_expansion(
                requirement=requirement,
                generated_output=story_expansion,
            )
        )

        task_result = (
            self.evaluate_task_breakdown(
                requirement=requirement,
                expanded_story=story_expansion,
                generated_output=task_breakdown,
            )
        )

        testcase_result = (
            self.evaluate_test_case_generation(
                requirement=requirement,
                generated_output=test_case_generation,
            )
        )

        return {
            "storyExpansion": story_result,
            "taskBreakdown": task_result,
            "testCaseGeneration": testcase_result,
        }

    # ==========================================================
    # REQUIREMENT CONTEXT
    # ==========================================================

    @staticmethod
    def _build_requirement_text(
        requirement,
    ) -> str:
        """
        Convert the Requirement model into semantic
        evaluation context.
        """

        acceptance_lines = []

        for acceptance_criteria in (
            requirement.acceptance_criteria or []
        ):
            acceptance_lines.append(
                (
                    f"{acceptance_criteria.acceptance_criteria_id}: "
                    f"{acceptance_criteria.title} - "
                    f"{acceptance_criteria.description}"
                )
            )

        acceptance_text = "\n".join(
            acceptance_lines
        )

        return (
            f"Requirement ID: "
            f"{requirement.requirement_id}\n"
            f"Requirement Type: "
            f"{requirement.requirement_type}\n"
            f"Title: {requirement.title}\n"
            f"Description: {requirement.description}\n"
            f"Business Rules: "
            f"{requirement.business_rules}\n"
            f"Priority: {requirement.priority}\n\n"
            f"Acceptance Criteria:\n"
            f"{acceptance_text}"
        )

    # ==========================================================
    # TEXT CONVERSION
    # ==========================================================

    @staticmethod
    def _to_text(
        value,
    ) -> str:
        """
        Convert an artifact into text for DeepEval.
        """

        if isinstance(value, str):
            return value

        if value is None:
            return ""

        import json

        return json.dumps(
            value,
            indent=2,
            ensure_ascii=False,
        )
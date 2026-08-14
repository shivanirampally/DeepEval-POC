from dataclasses import dataclass


@dataclass(slots=True)
class BenchmarkTestCase:
    """
    Represents an approved benchmark test case
    linked to an Acceptance Criteria.

    This is the AC-level benchmark used for
    testcase-level validation and DeepEval evaluation.
    """

    test_case_id: str
    acceptance_criteria_ref: str

    test_type: str
    technique: str
    priority: str

    description: str
    precondition: str
    test_data: str

    steps: list[str]

    expected_result: str

    deep_eval_reference: str = ""

    @property
    def benchmark_text(self) -> str:
        """
        Converts the benchmark test case into
        semantic text for DeepEval.
        """

        return (
            f"Test Case ID: {self.test_case_id}\n"
            f"Acceptance Criteria: "
            f"{self.acceptance_criteria_ref}\n"
            f"Test Type: {self.test_type}\n"
            f"Technique: {self.technique}\n"
            f"Priority: {self.priority}\n"
            f"Description: {self.description}\n"
            f"Precondition: {self.precondition}\n"
            f"Test Data: {self.test_data}\n"
            f"Steps:\n"
            f"{chr(10).join(self.steps)}\n"
            f"Expected Result: {self.expected_result}\n"
            f"DeepEval Reference: "
            f"{self.deep_eval_reference}"
        )
from dataclasses import dataclass


@dataclass(slots=True)
class UserStoryBenchmark:
    """
    Represents a benchmark scenario at the
    User Story / Requirement level.

    This is NOT an individual Acceptance Criteria
    test case.

    It represents the broader scenario coverage
    expected for a requirement.
    """

    benchmark_test_case_id: str
    requirement_id: str

    scenario: str
    category: str
    priority: str

    precondition: str
    test_data: str

    steps: list[str]

    expected_result: str

    source: str = ""
    deep_eval_reference: str = ""

    @property
    def benchmark_text(self) -> str:
        """
        Converts the User Story benchmark scenario
        into semantic text for evaluation.
        """

        return (
            f"Benchmark ID: "
            f"{self.benchmark_test_case_id}\n"
            f"Requirement ID: {self.requirement_id}\n"
            f"Scenario: {self.scenario}\n"
            f"Category: {self.category}\n"
            f"Priority: {self.priority}\n"
            f"Precondition: {self.precondition}\n"
            f"Test Data: {self.test_data}\n"
            f"Steps:\n"
            f"{chr(10).join(self.steps)}\n"
            f"Expected Result: {self.expected_result}\n"
            f"Source: {self.source}\n"
            f"DeepEval Reference: "
            f"{self.deep_eval_reference}"
        )
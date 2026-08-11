from dataclasses import dataclass


@dataclass(slots=True)
class BenchmarkTestCase:
    """
    Represents a benchmark test case used as the
    reference repository for evaluation.
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

    @property
    def benchmark_text(self) -> str:
        return (
            f"{self.description}\n"
            f"{self.expected_result}"
        )
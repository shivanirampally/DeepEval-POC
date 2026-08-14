from dataclasses import dataclass


@dataclass(slots=True)
class AcceptanceCriteria:
    """
    Represents one Acceptance Criteria belonging
    to a User Story.
    """

    acceptance_criteria_id: str

    title: str
    description: str

    business_rules: str
    priority: str

    benchmark_testcases: list = None

    def __post_init__(self):
        if self.benchmark_testcases is None:
            self.benchmark_testcases = []

    @property
    def testcase_count(self) -> int:
        return len(self.benchmark_testcases)
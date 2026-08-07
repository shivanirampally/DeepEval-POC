from dataclasses import dataclass


@dataclass(slots=True)
class GroundTruth:

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
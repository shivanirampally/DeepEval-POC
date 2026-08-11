from dataclasses import dataclass, field

from models.benchmark_testcase import BenchmarkTestCase


@dataclass(slots=True)
class Requirement:
    """
    Represents a business requirement.
    """

    requirement_id: str
    requirement_type: str
    title: str
    description: str
    business_rules: str
    priority: str

    benchmark_repository: list[BenchmarkTestCase] = field(
        default_factory=list
    )
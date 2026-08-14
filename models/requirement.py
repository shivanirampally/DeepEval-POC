from dataclasses import dataclass, field

from models.benchmark_testcase import BenchmarkTestCase
from models.user_story_benchmark import UserStoryBenchmark
from models.acceptance_criteria import AcceptanceCriteria


@dataclass(slots=True)
class Requirement:
    """
    Represents a top-level User Story / Requirement.

    Structure
    ---------
    Requirement
        |
        +-- User Story Benchmarks
        |
        +-- Acceptance Criteria
        |      |
        |      +-- Benchmark Test Cases
        |
        +-- Input Variations
        |
        +-- Usability / Navigation
        |
        +-- Non-Functional Scenarios

    Example
    -------
    US-001
        |
        +-- User Story Benchmarks
        |
        +-- AC-001
        |     +-- TC001
        |     +-- TC002
        |
        +-- AC-002
        |     +-- TC003
        |
        +-- AC-003
              +-- TC004
              +-- TC005
    """

    # ==========================================================
    # Requirement Information
    # ==========================================================

    requirement_id: str

    requirement_type: str

    title: str

    description: str

    business_rules: str

    priority: str

    # ==========================================================
    # User Story Benchmark Scenarios
    # ==========================================================

    user_story_benchmarks: list[
        UserStoryBenchmark
    ] = field(
        default_factory=list
    )

    # ==========================================================
    # Acceptance Criteria
    # ==========================================================

    acceptance_criteria: list[
        AcceptanceCriteria
    ] = field(
        default_factory=list
    )

    # ==========================================================
    # Input Variations
    # ==========================================================

    input_variations: list[dict] = field(
        default_factory=list
    )

    # ==========================================================
    # Usability / Navigation
    # ==========================================================

    usability_navigation: list[dict] = field(
        default_factory=list
    )

    # ==========================================================
    # Non-Functional Scenarios
    # ==========================================================

    non_functional: list[dict] = field(
        default_factory=list
    )

    # ==========================================================
    # Convenience Properties
    # ==========================================================

    @property
    def acceptance_criteria_count(self) -> int:
        """
        Number of Acceptance Criteria belonging
        to this User Story.
        """

        return len(
            self.acceptance_criteria
        )

    @property
    def user_story_benchmark_count(self) -> int:
        """
        Number of User Story benchmark scenarios.
        """

        return len(
            self.user_story_benchmarks
        )

    @property
    def acceptance_criteria_testcase_count(self) -> int:
        """
        Total number of benchmark test cases across
        all Acceptance Criteria.
        """

        return sum(
            len(
                acceptance_criteria
                .benchmark_testcases
            )
            for acceptance_criteria
            in self.acceptance_criteria
        )

    @property
    def input_variation_count(self) -> int:
        """
        Number of input variation scenarios.
        """

        return len(
            self.input_variations
        )

    @property
    def usability_scenario_count(self) -> int:
        """
        Number of usability/navigation scenarios.
        """

        return len(
            self.usability_navigation
        )

    @property
    def non_functional_count(self) -> int:
        """
        Number of non-functional scenarios.
        """

        return len(
            self.non_functional
        )

    @property
    def total_benchmark_testcases(self) -> int:
        """
        Total AC-level benchmark test cases.
        """

        return self.acceptance_criteria_testcase_count
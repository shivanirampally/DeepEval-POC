from dataclasses import dataclass


@dataclass(slots=True)
class Requirement:
    """
    Represents a business requirement.
    """

    requirement_id: str
    title: str
    acceptance_criteria: str
from dataclasses import dataclass


@dataclass(slots=True)
class Requirement:
    """
    Represents a business requirement used for
    LLM-based test case generation.
    """

    requirement_id: str
    title: str
    acceptance_criteria: str

    description: str = ""
    business_rules: str = ""
    module: str = ""
    priority: str = ""
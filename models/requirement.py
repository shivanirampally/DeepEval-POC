from dataclasses import dataclass


@dataclass(slots=True)
class Requirement:
    """
    Represents a business requirement used for
    LLM-based test case generation.
    """

    requirement_id: str
    requirement_type: str
    title: str
    description: str
    business_rules: str
    priority: str
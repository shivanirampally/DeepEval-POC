from dataclasses import dataclass
from models.ground_truth import GroundTruth

@dataclass(slots=True)
class Requirement:
    """
    Represents a business requirement used for
    LLM-based test case generation and evaluation.
    """

    requirement_id: str
    requirement_type: str
    title: str
    description: str
    business_rules: str
    priority: str

    ground_truth: list[GroundTruth] | None = None

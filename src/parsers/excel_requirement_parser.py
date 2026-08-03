from pathlib import Path
import pandas as pd
from src.models.requirement import Requirement
from src.config.settings import REQUIRED_COLUMNS

class ExcelRequirementParser:
    """
    Reads business requirements from an Excel file.
    """

    def parse(self, file_path: Path) -> list[Requirement]:

        dataframe = pd.read_excel(file_path)

        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in REQUIRED_COLUMNS
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        requirements = []

        for _, row in dataframe.iterrows():

            requirement = Requirement(
                requirement_id=str(row["Requirement ID"]).strip(),
                title=str(row["Title"]).strip(),
                acceptance_criteria=str(row["Acceptance Criteria"]).strip()
            )

            requirements.append(requirement)

        return requirements
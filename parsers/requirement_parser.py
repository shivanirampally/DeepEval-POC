from pathlib import Path
import pandas as pd
from config.settings import (REQUIREMENT_SHEET,REQUIRED_REQUIREMENT_COLUMNS,)
from models.requirement import Requirement


class RequirementParser:
    """
    Reads requirements from the workbook.
    """

    def parse(self, file_path: Path) -> list[Requirement]:

        dataframe = pd.read_excel(
            file_path,
            sheet_name=REQUIREMENT_SHEET,
        )

        missing_columns = [
            column
            for column in REQUIRED_REQUIREMENT_COLUMNS
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        requirements = []

        for _, row in dataframe.iterrows():

            requirements.append(
                Requirement(
                    requirement_id=str(row["Requirement ID"]).strip(),
                    requirement_type=str(row["Requirement Type"]).strip(),
                    title=str(row["Title"]).strip(),
                    description=str(
                        row["Description/Acceptance Criteria"]
                    ).strip(),
                    business_rules=str(row["Business Rules"]).strip(),
                    priority=str(row["Priority"]).strip(),
                )
            )

        return requirements
from pathlib import Path
import pandas as pd
from config.settings import (REQUIREMENT_SHEET, REQUIRED_REQUIREMENT_COLUMNS,)
from models.requirement import Requirement
from parsers.benchmark_repository_parser import BenchmarkRepositoryParser


class RequirementParser:
    """
    Reads Requirements sheet.

    Responsibilities
    ----------------
    • Read Requirement workbook
    • Validate required columns
    • Map Acceptance Criteria to Benchmark Repository
    • Return Requirement objects
    """

    def parse(self,file_path: Path,) -> list[Requirement]:

        # Read Requirement Sheet
        dataframe = pd.read_excel(file_path,sheet_name=REQUIREMENT_SHEET,)
        dataframe.columns = (dataframe.columns.astype(str).str.strip())

        # Validate Columns
        missing_columns = [
            column
            for column in REQUIRED_REQUIREMENT_COLUMNS
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(f"Missing Requirement Columns: {missing_columns}")

        # Read Benchmark Repository    
        benchmark_parser = BenchmarkRepositoryParser()
        benchmark_repository = (benchmark_parser.parse(file_path))

        # Build AC → TestCases Mapping    
        benchmark_map = {}
        for testcase in benchmark_repository:
            ac_ref = (testcase.acceptance_criteria_ref.strip().upper())
            benchmark_map.setdefault(ac_ref,[]).append(testcase)

        # Create Requirement Objects
        requirements = []
        for _, row in dataframe.iterrows():
            requirement_id = (self._clean_value(row["RequirementID"]).upper())

            requirement = Requirement(

                requirement_id=requirement_id,
                requirement_type=self._clean_value(
                    row["RequirementType"]
                ),

                title=self._clean_value(row["Title"]),
                description=self._clean_value(row["Description/AcceptanceCriteria"]),
                business_rules=self._clean_value(row["BusinessRules"]),
                priority=self._clean_value(row["Priority"]),
                benchmark_repository=benchmark_map.get(requirement_id,[],),
            )

            requirements.append(requirement)

        return requirements

    # Helper
    @staticmethod
    def _clean_value(value):

        if pd.isna(value): return ""
        value = str(value).strip()

        if value.lower() == "nan": return ""

        return value
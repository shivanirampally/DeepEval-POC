from pathlib import Path
import pandas as pd
from config.settings import (BENCHMARK_REPOSITORY_SHEET,)
from models.benchmark_testcase import (BenchmarkTestCase,)

class BenchmarkRepositoryParser:
    """
    Reads and normalizes the Benchmark Repository.

    Responsibilities
    ----------------
    • Read Benchmark Test Case sheet
    • Convert rows into BenchmarkTestCase objects
    • Provide benchmark content for semantic evaluation
    """

    def parse(self,file_path: Path,) -> list[BenchmarkTestCase]:
        dataframe = pd.read_excel(file_path, sheet_name=BENCHMARK_REPOSITORY_SHEET,)
        dataframe.columns = (dataframe.columns.astype(str).str.strip())

        benchmark_testcases = []

        for _, row in dataframe.iterrows():

            benchmark_testcase = BenchmarkTestCase(
                test_case_id=self._clean(row["TC ID"]),
                acceptance_criteria_ref=self._clean(row["AC Ref"]),
                test_type=self._clean(row["Test Type"]),
                technique=self._clean(row["Technique"]),
                priority=self._clean(row["Priority"]),
                description=self._clean(row["Description"]),
                precondition=self._clean(row["Precondition"]),
                test_data=self._clean(row["Test Data"]),
                steps=self._parse_steps(row["Steps"]),
                expected_result=self._clean(row["Expected Result"]),
            )

            benchmark_testcases.append(
                benchmark_testcase
            )

        return benchmark_testcases

    # ==========================================================
    # Benchmark Repository → Evaluation Text
    # ==========================================================

    @staticmethod
    def to_benchmark_text(
        benchmark_testcases: list[BenchmarkTestCase],
    ) -> str:

        output = []

        for testcase in benchmark_testcases:

            output.append(
                f"""
Test Case ID:
{testcase.test_case_id}

Description:
{testcase.description}

Precondition:
{testcase.precondition}

Test Data:
{testcase.test_data}

Steps:
{chr(10).join(testcase.steps)}

Expected Result:
{testcase.expected_result}
""".strip()
            )

        return "\n\n".join(output)

    # ==========================================================
    # Helpers
    # ==========================================================

    @staticmethod
    def _parse_steps(value):

        text = BenchmarkRepositoryParser._clean(
            value
        )

        if not text:
            return []

        return [
            step.strip()
            for step in text.split("\n")
            if step.strip()
        ]

    @staticmethod
    def _clean(value):

        if pd.isna(value):
            return ""

        value = str(value).strip()

        if value.lower() == "nan":
            return ""

        return value
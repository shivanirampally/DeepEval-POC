from pathlib import Path

import pandas as pd

from config.settings import (
    USER_STORY_BENCHMARK_SHEET,
    AC_BENCHMARK_SHEET,
    INPUT_VARIATION_SHEET,
    USABILITY_SHEET,
    NON_FUNCTIONAL_SHEET,
    REQUIRED_USER_STORY_BENCHMARK_COLUMNS,
    REQUIRED_AC_BENCHMARK_COLUMNS,
    REQUIRED_INPUT_VARIATION_COLUMNS,
    REQUIRED_USABILITY_COLUMNS,
    REQUIRED_NON_FUNCTIONAL_COLUMNS,
)

from models.benchmark_testcase import BenchmarkTestCase
from models.user_story_benchmark import UserStoryBenchmark


class BenchmarkRepositoryParser:
    """
    Reads and normalizes the complete benchmark repository.

    Repository structure
    --------------------

    02_UserStory_Benchmark
        |
        └── UserStoryBenchmark

    03_AC_Benchmark_TestCases
        |
        └── BenchmarkTestCase

    04_InputVariations
        |
        └── Input variation dictionaries

    05_UsabilityNavigation
        |
        └── Usability/navigation dictionaries

    06_NonFunctional
        |
        └── Non-functional dictionaries
    """

    # ==========================================================
    # User Story Benchmarks
    # ==========================================================

    def parse_user_story_benchmarks(
        self,
        file_path: Path,
    ) -> list[UserStoryBenchmark]:
        """
        Parse user-story-level benchmark scenarios.
        """

        dataframe = self._read_sheet(
            file_path,
            USER_STORY_BENCHMARK_SHEET,
        )

        self._validate_columns(
            dataframe,
            REQUIRED_USER_STORY_BENCHMARK_COLUMNS,
            USER_STORY_BENCHMARK_SHEET,
        )

        benchmarks = []

        for _, row in dataframe.iterrows():

            benchmark = UserStoryBenchmark(

                benchmark_test_case_id=self._clean(
                    row["Benchmark TC ID"]
                ),

                requirement_id=self._clean(
                    row["Requirement ID"]
                ).upper(),

                scenario=self._clean(
                    row["Scenario"]
                ),

                category=self._clean(
                    row["Category"]
                ),

                priority=self._clean(
                    row["Priority"]
                ),

                precondition=self._clean(
                    row["Precondition"]
                ),

                test_data=self._clean(
                    row["Test Data"]
                ),

                steps=self._parse_steps(
                    row["Steps"]
                ),

                expected_result=self._clean(
                    row["Expected Result"]
                ),

                source=self._clean(
                    row.get("Source", "")
                ),

                deep_eval_reference=self._to_bool(
                    row.get("DeepEval Reference", True)
                ),
            )

            benchmarks.append(benchmark)

        return benchmarks

    # ==========================================================
    # Acceptance Criteria Benchmarks
    # ==========================================================

    def parse_acceptance_criteria_benchmarks(
        self,
        file_path: Path,
    ) -> list[BenchmarkTestCase]:
        """
        Parse acceptance-criteria-level benchmark test cases.
        """

        dataframe = self._read_sheet(
            file_path,
            AC_BENCHMARK_SHEET,
        )

        self._validate_columns(
            dataframe,
            REQUIRED_AC_BENCHMARK_COLUMNS,
            AC_BENCHMARK_SHEET,
        )

        benchmarks = []

        for _, row in dataframe.iterrows():

            benchmark = BenchmarkTestCase(

                test_case_id=self._clean(
                    row["TC ID"]
                ),

                acceptance_criteria_ref=self._clean(
                    row["AC Ref"]
                ).upper(),

                test_type=self._clean(
                    row["Test Type"]
                ),

                technique=self._clean(
                    row["Technique"]
                ),

                priority=self._clean(
                    row["Priority"]
                ),

                description=self._clean(
                    row["Description"]
                ),

                precondition=self._clean(
                    row["Precondition"]
                ),

                test_data=self._clean(
                    row["Test Data"]
                ),

                steps=self._parse_steps(
                    row["Steps"]
                ),

                expected_result=self._clean(
                    row["Expected Result"]
                ),

                deep_eval_reference=self._to_bool(
                    row.get(
                        "DeepEval Reference",
                        True,
                    )
                ),
            )

            benchmarks.append(benchmark)

        return benchmarks

    # ==========================================================
    # Input Variations
    # ==========================================================

    def parse_input_variations(
        self,
        file_path: Path,
    ) -> list[dict]:
        """
        Parse input variation scenarios.

        These are stored separately from benchmark test cases.
        """

        dataframe = self._read_sheet(
            file_path,
            INPUT_VARIATION_SHEET,
        )

        self._validate_columns(
            dataframe,
            REQUIRED_INPUT_VARIATION_COLUMNS,
            INPUT_VARIATION_SHEET,
        )

        return self._dataframe_to_dicts(
            dataframe
        )

    # ==========================================================
    # Usability / Navigation
    # ==========================================================

    def parse_usability_navigation(
        self,
        file_path: Path,
    ) -> list[dict]:
        """
        Parse usability and navigation scenarios.
        """

        dataframe = self._read_sheet(
            file_path,
            USABILITY_SHEET,
        )

        self._validate_columns(
            dataframe,
            REQUIRED_USABILITY_COLUMNS,
            USABILITY_SHEET,
        )

        return self._dataframe_to_dicts(
            dataframe
        )

    # ==========================================================
    # Non Functional
    # ==========================================================

    def parse_non_functional(
        self,
        file_path: Path,
    ) -> list[dict]:
        """
        Parse non-functional scenarios.
        """

        dataframe = self._read_sheet(
            file_path,
            NON_FUNCTIONAL_SHEET,
        )

        self._validate_columns(
            dataframe,
            REQUIRED_NON_FUNCTIONAL_COLUMNS,
            NON_FUNCTIONAL_SHEET,
        )

        return self._dataframe_to_dicts(
            dataframe
        )

    # ==========================================================
    # Backward Compatibility
    # ==========================================================

    def parse(
        self,
        file_path: Path,
    ) -> list[BenchmarkTestCase]:
        """
        Backward-compatible parser.

        Existing code calling:

            BenchmarkRepositoryParser().parse(file)

        receives the acceptance-criteria benchmark test cases.

        New code should prefer:

            parse_acceptance_criteria_benchmarks()
            parse_user_story_benchmarks()
        """

        return self.parse_acceptance_criteria_benchmarks(
            file_path
        )

    # ==========================================================
    # Benchmark → Evaluation Text
    # ==========================================================

    @staticmethod
    def to_benchmark_text(
        benchmark_testcases: list[BenchmarkTestCase],
    ) -> str:
        """
        Convert acceptance-criteria benchmark test cases
        into semantic evaluation text.
        """

        output = []

        for testcase in benchmark_testcases:

            if not testcase.deep_eval_reference:
                continue

            output.append(
                testcase.benchmark_text
            )

        return "\n\n".join(output)

    # ==========================================================
    # User Story → Evaluation Text
    # ==========================================================

    @staticmethod
    def to_user_story_benchmark_text(
        benchmarks: list[UserStoryBenchmark],
    ) -> str:
        """
        Convert user-story benchmarks into semantic evaluation text.
        """

        output = []

        for benchmark in benchmarks:

            if not benchmark.deep_eval_reference:
                continue

            output.append(
                benchmark.benchmark_text
            )

        return "\n\n".join(output)

    # ==========================================================
    # Excel Helpers
    # ==========================================================

    @staticmethod
    def _read_sheet(
        file_path: Path,
        sheet_name: str,
    ) -> pd.DataFrame:

        try:

            dataframe = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
            )

        except ValueError as exception:

            raise ValueError(
                f"Required sheet '{sheet_name}' "
                f"was not found in workbook."
            ) from exception

        dataframe.columns = (
            dataframe.columns
            .astype(str)
            .str.strip()
        )

        return dataframe

    # ==========================================================
    # Column Validation
    # ==========================================================

    @staticmethod
    def _validate_columns(
        dataframe: pd.DataFrame,
        required_columns: list[str],
        sheet_name: str,
    ) -> None:

        missing_columns = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing_columns:

            raise ValueError(
                f"Missing columns in "
                f"'{sheet_name}': "
                f"{missing_columns}"
            )

    # ==========================================================
    # DataFrame → Dictionary
    # ==========================================================

    @classmethod
    def _dataframe_to_dicts(
        cls,
        dataframe: pd.DataFrame,
    ) -> list[dict]:

        records = []

        for record in dataframe.to_dict(
            orient="records"
        ):

            cleaned_record = {
                key: cls._clean(value)
                for key, value in record.items()
            }

            records.append(
                cleaned_record
            )

        return records

    # ==========================================================
    # Steps
    # ==========================================================

    @classmethod
    def _parse_steps(
        cls,
        value,
    ) -> list[str]:

        text = cls._clean(
            value
        )

        if not text:
            return []

        return [
            step.strip()
            for step in text.splitlines()
            if step.strip()
        ]

    # ==========================================================
    # Clean
    # ==========================================================

    @staticmethod
    def _clean(value) -> str:

        if pd.isna(value):
            return ""

        value = str(value).strip()

        if value.lower() == "nan":
            return ""

        return value

    # ==========================================================
    # Boolean
    # ==========================================================

    @staticmethod
    def _to_bool(value) -> bool:

        if isinstance(value, bool):
            return value

        if pd.isna(value):
            return False

        value = str(value).strip().lower()

        return value in {
            "yes",
            "true",
            "1",
            "y",
        }
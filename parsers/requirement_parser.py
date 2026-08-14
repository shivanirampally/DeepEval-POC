from pathlib import Path

import pandas as pd

from config.settings import (
    REQUIREMENT_SHEET,
    REQUIRED_REQUIREMENT_COLUMNS,
)

from models.requirement import Requirement

from models.acceptance_criteria import (
    AcceptanceCriteria,
)

from parsers.benchmark_repository_parser import (
    BenchmarkRepositoryParser,
)


class RequirementParser:
    """
    Reads the complete requirement repository
    and builds the User Story -> Acceptance Criteria
    -> Benchmark Test Case hierarchy.

    Repository Structure
    --------------------

    User Story
        |
        +-- User Story Benchmarks
        |
        +-- Acceptance Criteria
              |
              +-- AC Benchmark Test Cases

    Example
    -------

    US-001
        |
        +-- User Story Benchmarks
        |
        +-- AC-001
        |     +-- TC001
        |     +-- TC002
        |     +-- TC003
        |
        +-- AC-002
        |     +-- TC004
        |
        +-- AC-003
              +-- TC005
              +-- TC006

    Important
    ---------

    Only User Story rows become top-level Requirement
    objects.

    Acceptance Criteria rows are mapped underneath
    their parent User Story.
    """

    def parse(
        self,
        file_path: Path,
    ) -> list[Requirement]:

        # ======================================================
        # 1. Read Requirements Sheet
        # ======================================================

        dataframe = pd.read_excel(
            file_path,
            sheet_name=REQUIREMENT_SHEET,
        )

        dataframe.columns = (
            dataframe.columns
            .astype(str)
            .str.strip()
        )

        # ======================================================
        # 2. Validate Columns
        # ======================================================

        missing_columns = [
            column
            for column in REQUIRED_REQUIREMENT_COLUMNS
            if column not in dataframe.columns
        ]

        if missing_columns:

            raise ValueError(
                "Invalid Requirements sheet structure.\n"
                f"Sheet: {REQUIREMENT_SHEET}\n"
                f"Missing columns: {missing_columns}\n"
                f"Found columns: "
                f"{list(dataframe.columns)}"
            )

        # ======================================================
        # 3. Normalize Requirement Rows
        # ======================================================

        rows = []

        for _, row in dataframe.iterrows():

            requirement_id = (
                self._clean(
                    row["Requirement ID"]
                )
                .upper()
            )

            requirement_type = (
                self._clean(
                    row["Requirement Type"]
                )
            )

            if not requirement_id:
                continue

            rows.append(
                {
                    "id": requirement_id,
                    "type": requirement_type,
                    "title": self._clean(
                        row["Title"]
                    ),
                    "description": self._clean(
                        row[
                            "Description/Acceptance Criteria"
                        ]
                    ),
                    "business_rules": self._clean(
                        row["Business Rules"]
                    ),
                    "priority": self._clean(
                        row["Priority"]
                    ),
                }
            )

        # ======================================================
        # 4. Separate User Stories and Acceptance Criteria
        # ======================================================

        user_story_rows = [
            row
            for row in rows
            if row["type"].lower()
            in {
                "user story",
                "userstory",
            }
        ]

        acceptance_criteria_rows = [
            row
            for row in rows
            if row["type"].lower()
            in {
                "acceptance criteria",
                "acceptance_criteria",
                "acceptancecriteria",
            }
        ]

        # ======================================================
        # 5. Parse Benchmark Repository
        # ======================================================

        benchmark_parser = (
            BenchmarkRepositoryParser()
        )

        # ------------------------------------------------------
        # User Story Benchmarks
        # ------------------------------------------------------

        user_story_benchmarks = (
            benchmark_parser
            .parse_user_story_benchmarks(
                file_path
            )
        )

        # ------------------------------------------------------
        # AC Benchmarks
        # ------------------------------------------------------

        acceptance_criteria_benchmarks = (
            benchmark_parser
            .parse_acceptance_criteria_benchmarks(
                file_path
            )
        )

        # ------------------------------------------------------
        # Input Variations
        # ------------------------------------------------------

        input_variations = (
            benchmark_parser
            .parse_input_variations(
                file_path
            )
        )

        # ------------------------------------------------------
        # Usability / Navigation
        # ------------------------------------------------------

        usability_navigation = (
            benchmark_parser
            .parse_usability_navigation(
                file_path
            )
        )

        # ------------------------------------------------------
        # Non-Functional
        # ------------------------------------------------------

        non_functional = (
            benchmark_parser
            .parse_non_functional(
                file_path
            )
        )

        # ======================================================
        # 6. Build Requirements
        # ======================================================

        requirements = []

        for user_story in user_story_rows:

            requirement_id = user_story["id"]

            # ==================================================
            # User Story Benchmark Mapping
            # ==================================================

            mapped_user_story_benchmarks = [

                benchmark

                for benchmark
                in user_story_benchmarks

                if (
                    self._clean(
                        benchmark.requirement_id
                    ).upper()
                    == requirement_id
                )

            ]

            # ==================================================
            # Find Acceptance Criteria belonging to US
            # ==================================================

            mapped_ac_rows = (
                self._find_acceptance_criteria(
                    user_story,
                    acceptance_criteria_rows,
                )
            )

            # ==================================================
            # Build Acceptance Criteria Objects
            # ==================================================

            acceptance_criteria = []

            for ac_row in mapped_ac_rows:

                ac_id = ac_row["id"]

                # ----------------------------------------------
                # Map benchmark test cases to AC
                # ----------------------------------------------

                mapped_testcases = [

                    testcase

                    for testcase
                    in acceptance_criteria_benchmarks

                    if (
                        self._clean(
                            testcase
                            .acceptance_criteria_ref
                        ).upper()
                        == ac_id
                    )

                ]

                ac = AcceptanceCriteria(

                    acceptance_criteria_id=ac_id,

                    title=ac_row["title"],

                    description=ac_row[
                        "description"
                    ],

                    business_rules=ac_row[
                        "business_rules"
                    ],

                    priority=ac_row[
                        "priority"
                    ],

                    benchmark_testcases=(
                        mapped_testcases
                    ),
                )

                acceptance_criteria.append(
                    ac
                )

            # ==================================================
            # Additional Repository Mapping
            # ==================================================

            mapped_input_variations = [

                item

                for item
                in input_variations

                if (
                    self._clean(
                        item.get(
                            "Requirement ID"
                        )
                    ).upper()
                    == requirement_id
                )

            ]

            mapped_usability_navigation = [

                item

                for item
                in usability_navigation

                if (
                    self._clean(
                        item.get(
                            "Requirement ID"
                        )
                    ).upper()
                    == requirement_id
                )

            ]

            mapped_non_functional = [

                item

                for item
                in non_functional

                if (
                    self._clean(
                        item.get(
                            "Requirement ID"
                        )
                    ).upper()
                    == requirement_id
                )

            ]

            # ==================================================
            # Create Top-Level Requirement
            # ==================================================

            requirement = Requirement(

                requirement_id=requirement_id,

                requirement_type=user_story[
                    "type"
                ],

                title=user_story[
                    "title"
                ],

                description=user_story[
                    "description"
                ],

                business_rules=user_story[
                    "business_rules"
                ],

                priority=user_story[
                    "priority"
                ],

                user_story_benchmarks=(
                    mapped_user_story_benchmarks
                ),

                acceptance_criteria=(
                    acceptance_criteria
                ),

                input_variations=(
                    mapped_input_variations
                ),

                usability_navigation=(
                    mapped_usability_navigation
                ),

                non_functional=(
                    mapped_non_functional
                ),
            )

            requirements.append(
                requirement
            )

        return requirements

    # ==========================================================
    # Acceptance Criteria Mapping
    # ==========================================================

    @classmethod
    def _find_acceptance_criteria(
        cls,
        user_story,
        acceptance_criteria_rows,
    ):
        """
        Finds AC rows belonging to a User Story.

        Current workbook structure uses US-001 as the
        parent User Story and AC-001 ... AC-006 as
        Acceptance Criteria.

        Since the Requirements sheet does not contain
        an explicit Parent Requirement ID column, the
        mapping uses the workbook's AC identifier
        convention.

        Example:

            US-001
                AC-001
                AC-002
                AC-003
                AC-004
                AC-005
                AC-006
        """

        user_story_id = user_story["id"]

        # ------------------------------------------------------
        # For the current repository structure
        # ------------------------------------------------------

        if user_story_id.startswith("US-"):

            return [

                row

                for row
                in acceptance_criteria_rows

                if row["id"].startswith("AC-")

            ]

        return []

    # ==========================================================
    # Cleaning Helper
    # ==========================================================

    @staticmethod
    def _clean(value) -> str:

        if pd.isna(value):
            return ""

        value = str(value).strip()

        if value.lower() == "nan":
            return ""

        return value
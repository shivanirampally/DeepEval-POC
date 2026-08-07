from pathlib import Path

import pandas as pd

from config.settings import (
    GROUNDTRUTH_SHEET,
)

from models.ground_truth import GroundTruth


class GroundTruthParser:
    """
    Reads the Ground Truth repository.

    Returns
    -------
    List[GroundTruth]

    This parser is responsible only for reading and
    normalizing Ground Truth data.

    Requirement mapping is handled separately.
    """

    def parse(
        self,
        file_path: Path,
    ) -> list[GroundTruth]:

        dataframe = pd.read_excel(
            file_path,
            sheet_name=GROUNDTRUTH_SHEET,
        )

        dataframe.columns = (
            dataframe.columns.astype(str)
            .str.strip()
        )

        ground_truth_list = []

        for _, row in dataframe.iterrows():

            steps = self._parse_steps(
                row["Steps"]
            )

            ground_truth = GroundTruth(

                test_case_id=self._clean(
                    row["TC ID"]
                ),

                acceptance_criteria_ref=self._clean(
                    row["AC Ref"]
                ),

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

                steps=steps,

                expected_result=self._clean(
                    row["Expected Result"]
                ),

            )

            ground_truth_list.append(
                ground_truth
            )

        return ground_truth_list

    # ---------------------------------------------------------
    # Convert Ground Truth to semantic text for DeepEval
    # ---------------------------------------------------------

    @staticmethod
    def to_expected_output(
        ground_truth: list[GroundTruth],
    ) -> str:

        output = []

        for testcase in ground_truth:

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

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _parse_steps(value):

        text = GroundTruthParser._clean(
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
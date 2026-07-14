from pathlib import Path

import pandas as pd

from config.settings import REQUIRED_DATASET_COLUMNS


class ExcelReader:
    """
    Utility class for reading and validating AI test datasets.
    """

    @staticmethod
    def read_dataset(file_path):
        """
        Reads the Excel dataset and returns a validated Pandas DataFrame.
        """

        try:
            file_path = Path(file_path)

            # Check whether dataset exists
            if not file_path.exists():
                raise FileNotFoundError(
                    f"Dataset not found: {file_path}"
                )

            print("\n===================================")
            print("Reading AI Test Dataset")
            print("===================================")
            print(f"Dataset : {file_path}")

            dataframe = pd.read_excel(
                file_path,
                engine="openpyxl"
            )

            # Remove leading/trailing spaces from column names
            dataframe.columns = dataframe.columns.str.strip()

            # Check whether dataset is empty
            if dataframe.empty:
                raise ValueError(
                    "Dataset is empty. Please add test cases."
                )

            # Validate required columns
            missing_columns = [
                column
                for column in REQUIRED_DATASET_COLUMNS
                if column not in dataframe.columns
            ]

            if missing_columns:
                raise ValueError(
                    f"Missing required columns: {missing_columns}"
                )

            # Normalize text columns
            text_columns = [
                "Input",
                "Context",
                "Expected_Output",
                "AI_Response",
                "Result",
                "Remarks"
            ]

            for column in text_columns:
                if column in dataframe.columns:
                    dataframe[column] = (
                        dataframe[column]
                        .fillna("")
                        .astype(str)
                        .str.strip()
                    )

            print("\nDataset loaded successfully.")
            print(f"Dataset Size : {len(dataframe)} test cases")

            return dataframe

        except FileNotFoundError:
            raise

        except Exception as error:
            raise Exception(
                f"Failed to load dataset: {error}"
            )
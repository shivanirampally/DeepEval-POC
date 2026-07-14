from pathlib import Path
import pandas as pd

from config.settings import REQUIRED_DATASET_COLUMNS


class ExcelReader:
    """
    Utility class for reading AI test datasets from Excel.
    """

    @staticmethod
    def read_dataset(file_path):
        """
        Reads the Excel dataset and returns a Pandas DataFrame.
        """

        try:
            file_path = Path(file_path)

            if not file_path.exists():
                raise FileNotFoundError(
                    f"Dataset not found: {file_path}"
                )

            print("\nReading dataset from:")
            print(file_path)

            dataframe = pd.read_excel(
                file_path,
                engine="openpyxl"
            )

            if dataframe.empty:
                raise ValueError(
                    "Dataset is empty. Please add test cases."
                )

            missing_columns = [
                column
                for column in REQUIRED_DATASET_COLUMNS
                if column not in dataframe.columns
            ]

            if missing_columns:
                raise ValueError(
                    f"Missing required columns: {missing_columns}"
                )

            print("\nDataset loaded successfully.")
            print(f"Total Test Cases : {len(dataframe)}")

            return dataframe

        except FileNotFoundError as error:
            raise FileNotFoundError(error)

        except Exception as error:
            raise Exception(
                f"Failed to load dataset: {error}"
            )
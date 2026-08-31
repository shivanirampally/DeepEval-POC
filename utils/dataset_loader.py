import pandas as pd

from pathlib import Path

from utils.logger import (
    info,
    success,
)


def load_all_datasets(path):

    info("Loading Dataset...")
    info(f"Reading Excel: {Path(path).resolve()}")

    dataset = []

    for sheet_name in pd.ExcelFile(path).sheet_names:

        dataframe = pd.read_excel(
            path,
            sheet_name=sheet_name,
        )

        for _, row in dataframe.iterrows():

            dataset.append(
                {
                    "category": row["Hallucination_Type"],
                    "input": row["Input"],
                    "context": [row["Context"]],
                    "expected_output": row["Expected_Output"],
                }
            )

    success(
        f"Dataset Loaded ({len(dataset)} test cases)"
    )

    return dataset
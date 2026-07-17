import pandas as pd
from pathlib import Path

def load_all_datasets(path):

    print("Reading Excel File:")
    print(Path(path).resolve())

    excel_file = pd.ExcelFile(path)

    dataset = []

    for sheet_name in excel_file.sheet_names:

        df = pd.read_excel(
            path,
            sheet_name=sheet_name
        )

        print("Columns:", df.columns.tolist())

        for _, row in df.iterrows():

            dataset.append({
                "category": row["Hallucination_Type"],
                "input": row["Input"],
                "context": [row["Context"]],
                "expected_output": row["Expected_Output"]
            })

    return dataset
import pandas as pd


def load_all_datasets(path):

    excel_file = pd.ExcelFile(path)

    dataset = []

    for sheet_name in excel_file.sheet_names:

        df = pd.read_excel(
            path,
            sheet_name=sheet_name
        )

        for _, row in df.iterrows():

            dataset.append({

                "category": sheet_name,

                "input": row["Input"],

                "context": [row["Context"]]

            })

    return dataset
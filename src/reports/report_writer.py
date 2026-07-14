from pathlib import Path

import pandas as pd


class ReportWriter:
    """
    Writes AI evaluation results to an Excel report.
    """

    @staticmethod
    def save_report(
        dataframe,
        output_path
    ):

        try:

            output_path = Path(output_path)

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            dataframe.to_excel(
                output_path,
                index=False,
                engine="openpyxl"
            )

            print("\n===================================")
            print("Evaluation Report Generated")
            print("===================================")
            print(f"Location : {output_path}")
            print(f"Records  : {len(dataframe)}")
            print("===================================\n")

        except Exception as error:

            raise Exception(
                f"Failed to generate evaluation report: {error}"
            )
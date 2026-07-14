from config.settings import (
    INPUT_DATASET,
    OUTPUT_REPORT
)

from data.excel_reader import ExcelReader
from reports.report_writer import ReportWriter
from services.ai_evaluation_service import AIEvaluationService


def main():
    """
    Entry point for the AI Evaluation POC.
    """

    try:

        print("\n===== DeepEval POC =====")

        # Read Dataset
        dataframe = ExcelReader.read_dataset(
            INPUT_DATASET
        )

        # Generate AI Responses + Evaluate
        dataframe = AIEvaluationService.run(
            dataframe
        )

        # Generate Report
        ReportWriter.save_report(
            dataframe,
            OUTPUT_REPORT
        )

        print("\n===== Process Completed Successfully =====")

    except Exception as error:

        print("\n===================================")
        print("Application Failed")
        print("===================================")
        print(error)
        print("===================================\n")


if __name__ == "__main__":
    main()
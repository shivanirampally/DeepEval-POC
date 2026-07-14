from config.settings import (
    INPUT_DATASET,
    OUTPUT_REPORT
)

from data.excel_reader import ExcelReader
from reports.report_writer import ReportWriter
from services.ai_evaluation_service import AIEvaluationService


def main():

    print("===== DeepEval POC =====")

    dataframe = ExcelReader.read_dataset(
        INPUT_DATASET
    )

    dataframe = AIEvaluationService.run(
        dataframe
    )

    ReportWriter.save_report(
        dataframe,
        OUTPUT_REPORT
    )

    print("\n===== Process Completed Successfully =====")


if __name__ == "__main__":
    main()
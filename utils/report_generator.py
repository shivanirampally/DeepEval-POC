from datetime import datetime
from pathlib import Path
import pandas as pd
from config.app_config import REPORT_FOLDER
from utils.logger import (info,success,)


results_data = []

def get_severity(score):
    percentage = score * 100

    if percentage <= 20:
        return "Low"

    if percentage <= 50:
        return "Medium"

    if percentage <= 80:
        return "High"

    return "Critical"


def get_severity_score(severity):
    return {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4,
    }.get(severity, 0)


def add_result(
    category,
    prompt,
    context,
    expected_output,
    actual_output,
    result,
):
    hallucination_score = result["hallucination_score"]
    severity = get_severity(hallucination_score)
    severity_score = get_severity_score(severity)

    results_data.append(
        {
            "Category": category,
            "Question": prompt,
            "Context": context,
            "Expected Output": expected_output,
            "LLM Response": actual_output,
            "Hallucination Score": hallucination_score,
            "Correctness Score": result["correctness_score"],
            "Answer Relevancy Score": result["answer_relevancy_score"],
            "Hallucination Reason": result["hallucination_reason"],
            "Correctness Reason": result["correctness_reason"],
            "Answer Relevancy Reason": result["answer_relevancy_reason"],
            "Severity": severity,
            "Severity Score": severity_score,
        }
    )

    return severity, severity_score


def generate_excel_report(results):

    info("Generating Excel Report...")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_folder = (Path(REPORT_FOLDER) / timestamp)
    report_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path = (report_folder / "evaluation_report.xlsx")
    if not results:
        _write_empty_report(report_path)
        success(f"Excel Report Generated: {report_path}")
        return report_path

    summary_data = []
    with pd.ExcelWriter(
        report_path,
        engine="openpyxl",
    ) as writer:

        dataframe = pd.DataFrame(results)

        for category, category_data in dataframe.groupby(
            "Category"
        ):

            category_data.to_excel(
                writer,
                sheet_name=str(category)[:31],
                index=False,
            )

            summary_data.append(
                {
                    "Category": category,
                    "Total Cases": len(category_data),
                    "Average Hallucination Score": round(
                        category_data["Hallucination Score"].mean(),
                        2,
                    ),
                    "Average Correctness Score": round(
                        category_data["Correctness Score"].mean(),
                        2,
                    ),
                    "Average Answer Relevancy Score": round(
                        category_data["Answer Relevancy Score"].mean(),
                        2,
                    ),
                }
            )

        summary_dataframe = pd.DataFrame(summary_data)
        summary_dataframe.loc[len(summary_dataframe)] = {
            "Category": "OVERALL",
            "Total Cases": summary_dataframe[
                "Total Cases"
            ].sum(),
            "Average Hallucination Score": round(
                dataframe["Hallucination Score"].mean(),2,
            ),
            "Average Correctness Score": round(
                dataframe["Correctness Score"].mean(),2,
            ),
            "Average Answer Relevancy Score": round(
                dataframe["Answer Relevancy Score"].mean(),2,
            ),
        }

        summary_dataframe.to_excel(writer,sheet_name="Summary",index=False,)

    success(f"Excel Report Generated: {report_path}")
    return report_path


def _write_empty_report(path):

    with pd.ExcelWriter(path,engine="openpyxl",) as writer:
        pd.DataFrame(
            [
                {
                    "Status": ("No test results were available")
                }
            ]
        ).to_excel(writer,sheet_name="Summary",index=False,)
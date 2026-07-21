import pandas as pd

from pathlib import Path
from datetime import datetime

from config.app_config import REPORT_FOLDER

from utils.logger import (
    info,
    success,
)

results_data = []


def add_result(
    category,
    prompt,
    context,
    expected_output,
    actual_output,
    result,
    severity,
    severity_score,
):
    results_data.append(
        {
            "Category": category,
            "Question": prompt,
            "Context": context,
            "Expected Output": expected_output,
            "LLM Response": actual_output,
            "Hallucination Score": result["hallucination_score"],
            "Correctness Score": result["correctness_score"],
            "Answer Relevancy Score": result["answer_relevancy_score"],
            "Hallucination Reason": result["hallucination_reason"],
            "Correctness Reason": result["correctness_reason"],
            "Answer Relevancy Reason": result["answer_relevancy_reason"],
            "Severity": severity,
            "Severity Score": severity_score,
        }
    )


def generate_excel_report(results):

    info("Generating Excel Report...")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    report_folder = Path(REPORT_FOLDER) / timestamp
    report_folder.mkdir(parents=True, exist_ok=True)

    excel_path = report_folder / "hallucination_report.xlsx"

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:

        if not results:

            pd.DataFrame(
                [
                    {
                        "Status": "No test results were available"
                    }
                ]
            ).to_excel(
                writer,
                sheet_name="Summary",
                index=False,
            )

        else:

            summary_data = []

            categories = sorted(
                set(result["Category"] for result in results)
            )

            for category in categories:

                category_data = [
                    result
                    for result in results
                    if result["Category"] == category
                ]

                df = pd.DataFrame(category_data)

                avg_hallucination = round(
                    df["Hallucination Score"].mean(),
                    2,
                )

                avg_correctness = round(
                    df["Correctness Score"].mean(),
                    2,
                )

                avg_relevancy = round(
                    df["Answer Relevancy Score"].mean(),
                    2,
                )

                df.to_excel(
                    writer,
                    sheet_name=str(category)[:31],
                    index=False,
                )

                summary_data.append(
                    {
                        "Category": category,
                        "Total Cases": len(df),
                        "Average Hallucination Score": avg_hallucination,
                        "Average Correctness Score": avg_correctness,
                        "Average Answer Relevancy Score": avg_relevancy,
                    }
                )

            summary_df = pd.DataFrame(summary_data)

            overall_row = {
                "Category": "OVERALL",
                "Total Cases": summary_df["Total Cases"].sum(),
                "Average Hallucination Score": round(
                    summary_df["Average Hallucination Score"].mean(),
                    2,
                ),
                "Average Correctness Score": round(
                    summary_df["Average Correctness Score"].mean(),
                    2,
                ),
                "Average Answer Relevancy Score": round(
                    summary_df["Average Answer Relevancy Score"].mean(),
                    2,
                ),
            }

            summary_df.loc[len(summary_df)] = overall_row

            summary_df.to_excel(
                writer,
                sheet_name="Summary",
                index=False,
            )

    success(f"Excel Report Generated: {excel_path}")

    return excel_path
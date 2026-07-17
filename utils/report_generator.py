import pandas as pd
from pathlib import Path
from datetime import datetime

results_data = []


def generate_excel_report(results):

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    report_folder = Path("execution_reports") / timestamp
    report_folder.mkdir(parents=True, exist_ok=True)

    excel_path = report_folder / "hallucination_report.xlsx"

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:

        if not results:

            pd.DataFrame([{
                "Status": "No test results were available"
            }]).to_excel(
                writer,
                sheet_name="Summary",
                index=False
            )

        else:

            summary_data = []

            for category in sorted(set(r["Category"] for r in results)):

                category_data = [
                    r for r in results
                    if r["Category"] == category
                ]

                df = pd.DataFrame(category_data)

                avg_hallucination = round(
                    df["Hallucination Score"].mean(),
                    2
                )

                avg_correctness = round(
                    df["Correctness Score"].mean(),
                    2
                )

                avg_relevancy = round(
                    df["Answer Relevancy Score"].mean(),
                    2
                )

                df.to_excel(
                    writer,
                    sheet_name=str(category)[:31],
                    index=False
                )

                summary_data.append({

                    "Category": category,

                    "Total Cases": len(df),

                    "Average Hallucination Score": avg_hallucination,

                    "Average Correctness Score": avg_correctness,

                    "Average Answer Relevancy Score": avg_relevancy

                })

            summary_df = pd.DataFrame(summary_data)

            overall_row = {

                "Category": "OVERALL",

                "Total Cases": summary_df["Total Cases"].sum(),

                "Average Hallucination Score": round(
                    summary_df["Average Hallucination Score"].mean(),
                    2
                ),

                "Average Correctness Score": round(
                    summary_df["Average Correctness Score"].mean(),
                    2
                ),

                "Average Answer Relevancy Score": round(
                    summary_df["Average Answer Relevancy Score"].mean(),
                    2
                )

            }

            summary_df.loc[len(summary_df)] = overall_row

            summary_df.to_excel(
                writer,
                sheet_name="Summary",
                index=False
            )

    print(f"\nExcel Report Generated: {excel_path}")
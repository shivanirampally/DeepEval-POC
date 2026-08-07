import json
from pathlib import Path
from datetime import datetime

import pandas as pd

from config.settings import OUTPUT_FOLDER
from utils.logger import info, success


class ReportGenerator:
    """
    Generates the final enterprise evaluation report.
    """

    @staticmethod
    def generate(results):

        info("Generating Evaluation Report...")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        report_folder = Path(OUTPUT_FOLDER) / "reports"
        report_folder.mkdir(parents=True, exist_ok=True)

        report_path = (
            report_folder /
            f"llm_evaluation_report_{timestamp}.xlsx"
        )

        summary_rows = []
        validation_rows = []
        deepeval_rows = []
        testcase_rows = []

        for result in results:

            # -----------------------------
            # Summary
            # -----------------------------

            summary_rows.append({

                "Requirement ID":
                    result["requirementId"],

                "Generator":
                    result["generator"],

                "Framework Score":
                    result["overall"]["framework_score"],

                "DeepEval Score":
                    result["overall"]["deepeval_score"],

                "Overall Score":
                    result["overall"]["overall_score"],

                "Status":
                    result["overall"]["status"],

            })

            # -----------------------------
            # Framework Validation
            # -----------------------------

            validation_rows.append({

                "Requirement ID":
                    result["requirementId"],

                "Schema Score":
                    result["schemaValidation"]["score"],

                "TestCase Score":
                    result["testCaseValidation"]["score"],

                "Coverage Score":
                    result["coverageValidation"]["score"],

                "Schema Errors":
                    "\n".join(
                        result["schemaValidation"].get(
                            "errors",
                            [],
                        )
                    ),

                "TestCase Errors":
                    "\n".join(
                        result["testCaseValidation"].get(
                            "errors",
                            [],
                        )
                    ),

                "Coverage Warnings":
                    "\n".join(
                        result["coverageValidation"].get(
                            "warnings",
                            [],
                        )
                    ),

            })

            # -----------------------------
            # DeepEval
            # -----------------------------

            deepeval_rows.append({

                "Requirement ID":
                    result["requirementId"],

                "Hallucination":
                    result["deepEval"]["hallucination"]["score"],

                "Correctness":
                    result["deepEval"]["correctness"]["score"],

                "Answer Relevancy":
                    result["deepEval"]["answer_relevancy"]["score"],

                "Hallucination Reason":
                    result["deepEval"]["hallucination"]["reason"],

                "Correctness Reason":
                    result["deepEval"]["correctness"]["reason"],

                "Relevancy Reason":
                    result["deepEval"]["answer_relevancy"]["reason"],

            })

            # -----------------------------
            # Generated JSON
            # -----------------------------

            testcase_rows.append({

                "Requirement ID":
                    result["requirementId"],

                "Generated TestCases":
                    json.dumps(
                        result["generatedJson"],
                        indent=2,
                    ),

                "Ground Truth":
                    result["groundTruth"],

            })

        with pd.ExcelWriter(
            report_path,
            engine="openpyxl",
        ) as writer:

            pd.DataFrame(summary_rows).to_excel(
                writer,
                sheet_name="Summary",
                index=False,
            )

            pd.DataFrame(validation_rows).to_excel(
                writer,
                sheet_name="Framework Validation",
                index=False,
            )

            pd.DataFrame(deepeval_rows).to_excel(
                writer,
                sheet_name="DeepEval Metrics",
                index=False,
            )

            pd.DataFrame(testcase_rows).to_excel(
                writer,
                sheet_name="Generated TestCases",
                index=False,
            )

        success(
            f"Evaluation Report Generated : {report_path}"
        )

        return report_path
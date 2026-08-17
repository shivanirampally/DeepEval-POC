from pathlib import Path

from config.settings import (
    INPUT_WORKBOOK,
    MAX_REQUIREMENTS,
)

from parsers.requirement_parser import (
    RequirementParser,
)

from loaders.qa_boat_excel_loader import (
    QABoatExcelLoader,
)

from services.evaluation_json_builder import (
    EvaluationJsonBuilder,
)

from evaluators.llm_evaluator import (
    LLMEvaluator,
)

from reports.report_generator import (
    ReportGenerator,
)

from utils.logger import (
    header,
    info,
    success,
    warning,
    failed,
    evaluation_summary,
)


# ==========================================================
# QA BOAT EXCEL INPUT
# ==========================================================
#
# Change ONLY this path if your exported QA Boat file
# has a different name/location.
#
QA_BOAT_EXCEL = (
    "input/qa_boat/DeepEval-login-scenarios-2026-08-17-07-03-32.xlsx"
)

GENERATOR_NAME = "QA Boat"


def main():

    header(
        "QA BOAT EXCEL → DEEPEVAL EVALUATION"
    )

    # ======================================================
    # 1. Load Requirement Repository
    # ======================================================

    info("Loading requirement repository...")

    parser = RequirementParser()

    requirements = parser.parse(
        Path(INPUT_WORKBOOK)
    )

    if MAX_REQUIREMENTS:
        requirements = requirements[
            :MAX_REQUIREMENTS
        ]

    if not requirements:
        raise ValueError(
            "No requirements found in requirement repository."
        )

    success(
        f"Requirements Loaded : "
        f"{len(requirements)}"
    )

    # ======================================================
    # 2. Load QA Boat Excel
    # ======================================================

    info(
        f"Loading QA Boat Excel : "
        f"{QA_BOAT_EXCEL}"
    )

    generated_output = (
        QABoatExcelLoader.load(
            QA_BOAT_EXCEL
        )
    )

    test_cases = generated_output.get(
        "testCases",
        [],
    )

    if not test_cases:
        raise ValueError(
            "QA Boat Excel did not contain any test cases."
        )

    success(
        f"QA Boat Test Cases Loaded : "
        f"{len(test_cases)}"
    )

    # ======================================================
    # 3. Select Requirement
    # ======================================================
    #
    # The current QA Boat export does not contain the
    # Requirement ID directly. Therefore:
    #
    # - If the repository contains one requirement,
    #   use it automatically.
    #
    # - If there are multiple requirements, stop instead
    #   of blindly evaluating against the wrong requirement.
    #
    # ======================================================

    if len(requirements) == 1:

        requirement = requirements[0]

    else:

        raise ValueError(
            "Multiple requirements were found in the "
            "requirement repository, but the QA Boat Excel "
            "does not provide a direct Requirement ID mapping. "
            "Add explicit requirement mapping before running "
            "the evaluation."
        )

    success(
        f"Evaluation Requirement : "
        f"{requirement.requirement_id}"
    )

    # ======================================================
    # 4. Build Evaluation JSON
    # ======================================================
    #
    # Reuse the existing EvaluationJsonBuilder.
    #
    # This is important because we do NOT want to create
    # another evaluation data format just for QA Boat.
    #
    # The loader provides:
    #
    #     {"testCases": [...]}
    #
    # and the builder adds the requirement + benchmark
    # information required by DeepEval.
    #
    # ======================================================

    info(
        "Building evaluation data..."
    )

    evaluation_output = (
        EvaluationJsonBuilder.build(
            requirement=requirement,
            generated_output=generated_output,
        )
    )

    success(
        "Evaluation data ready."
    )

    # ======================================================
    # 5. Initialize Evaluator
    # ======================================================

    evaluator = LLMEvaluator()

    # ======================================================
    # 6. Run Evaluation
    # ======================================================

    info(
        "Running QA Boat evaluation..."
    )

    result = evaluator.evaluate(
        generator=GENERATOR_NAME,
        requirement=requirement,
        generated_output=generated_output,
        evaluation_output=evaluation_output,
    )

    success(
        "QA Boat evaluation completed."
    )

    # ======================================================
    # 7. Console Summary
    # ======================================================

    evaluation_summary(
        result
    )

    # ======================================================
    # 8. Generate Report
    # ======================================================

    info(
        "Generating QA Boat evaluation report..."
    )

    report_path = (
        ReportGenerator.generate(
            [result]
        )
    )

    success(
        f"QA Boat Evaluation Report : "
        f"{report_path}"
    )

    # ======================================================
    # 9. Completed
    # ======================================================

    header(
        "QA BOAT EVALUATION COMPLETED"
    )


if __name__ == "__main__":
    try:

        main()

    except Exception as exception:

        failed(
            f"QA Boat Evaluation Failed : "
            f"{exception}"
        )

        raise
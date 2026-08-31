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
    failed,
)


QA_BOAT_EXCEL = (
    "input/qa_boat/"
    "DeepEval-login-scenarios-2026-08-17-07-03-32.xlsx"
)

GENERATOR_NAME = "QA Boat"


def main():

    header(
        "QA BOAT → DEEPEVAL EVALUATION"
    )

    # ==========================================================
    # 1. Load Requirement Repository
    # ==========================================================

    info(
        "Loading requirement repository..."
    )

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

    # ==========================================================
    # 2. Load QA Boat Output
    # ==========================================================

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

    # ==========================================================
    # 3. Select Requirement
    # ==========================================================

    if len(requirements) == 1:

        requirement = requirements[0]

    else:

        raise ValueError(
            "Multiple requirements were found in the "
            "requirement repository, but the QA Boat Excel "
            "does not provide direct Requirement ID mapping."
        )

    success(
        f"Evaluation Requirement : "
        f"{requirement.requirement_id}"
    )

    # ==========================================================
    # 4. Build Evaluation Data
    # ==========================================================

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

    # ==========================================================
    # 5. Run Evaluation
    # ==========================================================

    evaluator = LLMEvaluator()

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

    # ==========================================================
    # 6. Generate Report
    # ==========================================================

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
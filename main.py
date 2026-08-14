from pathlib import Path
import time

from config.settings import (
    INPUT_WORKBOOK,
    OLLAMA_MODEL,
    MAX_REQUIREMENTS,
)

from parsers.requirement_parser import (
    RequirementParser,
)

from prompts.generation_prompt import (
    GenerationPromptBuilder,
)

from services.llm_service import (
    LLMService,
)

from services.generated_json_storage import (
    GeneratedJsonStorage,
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


GENERATOR_NAME = "QA Boat"


def main():

    header("QA BOAT → DEEPEVAL POC")

    # ==========================================================
    # 1. Load Requirements
    # ==========================================================

    parser = RequirementParser()

    requirements = parser.parse(
        Path(INPUT_WORKBOOK)
    )

    if MAX_REQUIREMENTS:
        requirements = requirements[
            :MAX_REQUIREMENTS
        ]

    success(
        f"Requirements Loaded : "
        f"{len(requirements)}"
    )

    # ==========================================================
    # 2. Initialize Evaluation Engine
    # ==========================================================

    evaluator = LLMEvaluator()

    evaluation_results = []

    # ==========================================================
    # 3. Process Requirements
    # ==========================================================

    for requirement in requirements:

        header(
            f"Processing : "
            f"{requirement.requirement_id}"
        )

        start_time = time.perf_counter()

        try:

            # ==================================================
            # Prompt Generation
            # ==================================================

            info ("Building prompt...")

            prompt = (
                GenerationPromptBuilder.build(
                    requirement
                )
            )

            # ==================================================
            # Generate Test Cases
            # ==================================================

            info("Generating test cases...")

            response = (
                LLMService.generate_response(
                    prompt=prompt,
                    model=OLLAMA_MODEL,
                )
            )

            success("Test cases generated.")
            # ==================================================
            # Save RAW Qwen3 JSON
            # ==================================================

            json_path = (
                GeneratedJsonStorage.save(
                    provider=GENERATOR_NAME,
                    requirement_id=(
                        requirement.requirement_id
                    ),
                    response=response,
                )
            )

            success(f"Generated JSON saved: {json_path}")

            # ==================================================
            # Load RAW Generated JSON
            # ==================================================

            generated_output = (
                GeneratedJsonStorage.load(
                    json_path
                )
            )

            # ==================================================
            # Build Evaluation JSON
            # ==================================================

            info("Building evaluation data...")

            evaluation_output = (
                EvaluationJsonBuilder.build(
                    requirement=requirement,
                    generated_output=generated_output,
                )
            )

            success("Evaluation data ready.")

            # ==================================================
            # Evaluation Engine
            # ==================================================

            info("Running evaluation...")

            result = evaluator.evaluate(

                generator=GENERATOR_NAME,

                requirement=requirement,

                generated_output=generated_output,
                evaluation_output=evaluation_output,


            )
            
            # ==================================================
            # Execution Time
            # ==================================================

            result[
                "overall"
            ][
                "execution_time"
            ] = round(
                time.perf_counter()
                - start_time,
                2,
            )

            # ==================================================
            # Store Result
            # ==================================================

            evaluation_results.append(
                result
            )

            # ==================================================
            # Console Summary
            # ==================================================

            evaluation_summary(
                result
            )

        except Exception as exception:

            failed(
                f"Requirement Evaluation Failed : "
                f"{exception}"
            )

            warning(
                f"Skipping Requirement : "
                f"{requirement.requirement_id}"
            )

            continue

    # ==========================================================
    # 4. Generate Excel Report
    # ==========================================================

    if evaluation_results:

        success(
            "Generating Evaluation Report..."
        )

        report_path = (
            ReportGenerator.generate(
                evaluation_results
            )
        )

        success(
            f"Evaluation Report : "
            f"{report_path}"
        )

    else:

        warning(
            "No evaluation results available."
        )

    # ==========================================================
    # 5. Execution Completed
    # ==========================================================

    header(
        "Execution Completed"
    )


if __name__ == "__main__":
    main()
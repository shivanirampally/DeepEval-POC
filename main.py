from pathlib import Path
import time
from config.settings import (INPUT_WORKBOOK,OLLAMA_MODEL,MAX_REQUIREMENTS,)
from parsers.requirement_parser import RequirementParser
from prompts.generation_prompt import GenerationPromptBuilder
from services.llm_service import LLMService
from services.json_storage import JsonStorage
from evaluators.llm_evaluator import LLMEvaluator
from reports.report_generator import ReportGenerator
from utils.logger import (header,success,warning,failed,evaluation_summary,)


GENERATOR_Name = "QA Boat"

def main():
    header("QA BOAT → DEEPEVAL POC")

    # Load Requirements
    parser = RequirementParser()
    requirements = parser.parse(Path(INPUT_WORKBOOK))
    if MAX_REQUIREMENTS: requirements = requirements[:MAX_REQUIREMENTS]
    success(f"Requirements Loaded : {len(requirements)}")
    evaluator = LLMEvaluator()
    evaluation_results = []

    # Process Requirements
    for requirement in requirements:
        header(f"Processing : {requirement.requirement_id}")
        start_time = time.perf_counter()

        try:
            # Prompt Generation
            success("Building Prompt...")
            prompt = GenerationPromptBuilder.build(requirement)

            # Generate Test Cases
            success("Generating Test Cases...")
            response = LLMService.generate_response(prompt=prompt,model=OLLAMA_MODEL,)

            # Save JSON
            json_path = JsonStorage.save(
                provider=GENERATOR_Name,
                requirement_id=requirement.requirement_id,
                response=response,
            )

            success(f"JSON Saved : {json_path}")

            # Load JSON
            generated_output = JsonStorage.load(json_path)

            # Evaluation          
            success("Running Evaluation Engine...")
            result = evaluator.evaluate(
                generator=GENERATOR_Name,
                requirement=requirement,
                generated_output=generated_output,
            )

            # Execution Time
            result["overall"]["execution_time"] = round(
                time.perf_counter() - start_time,2,)
            
            evaluation_results.append(result)
            evaluation_summary(result)

        except Exception as exception:
            failed(str(exception))
            warning(
                f"Skipping Requirement : "
                f"{requirement.requirement_id}"
            )

            continue

    # Generate Report
    if evaluation_results:
        report_path = ReportGenerator.generate(evaluation_results)
        success(f"Evaluation Report : {report_path}")

    else:
        warning("No evaluation results available.")
    header("Execution Completed")


if __name__ == "__main__":
    main()
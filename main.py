from config.app_config import (DATASET_PATH, MAX_TESTS,)
from generators.ollama_generator import generate_response
from evaluators.hallucination_evaluator import (HallucinationEvaluator,)
from utils.dataset_loader import load_all_datasets
from utils.report_generator import (add_result, generate_excel_report, results_data,)
from utils.logger import (header,info,success,summary,)


def main():
    header("AI HALLUCINATION EVALUATION")
    dataset = load_all_datasets(DATASET_PATH)

    if MAX_TESTS:
        dataset = dataset[:MAX_TESTS]
    evaluator = HallucinationEvaluator()

    for data in dataset:
        category = data["category"]
        prompt = data["input"]
        context = data["context"]
        expected_output = data["expected_output"]

        info(f"Running test case : {category}")
        actual_output = generate_response(prompt)

        result = evaluator.evaluate(
            input_text=prompt,
            actual_output_text=actual_output,
            context=context,
            expected_output=expected_output,
        )

        if result["status"] == "FAILED":
            info(f"Evaluation failed : "f"{result['error']}")
            continue

        severity, severity_score = add_result(
            category=category,
            prompt=prompt,
            context=context,
            expected_output=expected_output,
            actual_output=actual_output,
            result=result,
        )

        summary(
            category=category,
            hallucination=result["hallucination_score"],
            correctness=result["correctness_score"],
            relevancy=result["answer_relevancy_score"],
            severity=severity,
            severity_score=severity_score,
        )

    report_path = generate_excel_report(results_data)

    success(f"Report Location : {report_path}")
    header("EVALUATION COMPLETED")

if __name__ == "__main__":
    main()
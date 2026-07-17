import pytest

from utils.dataset_loader import load_all_datasets
from config.ollama_config import generate_response
from evaluators.hallucination_evaluator import HallucinationEvaluator
from utils.severity_utils import (
    get_severity,
    get_severity_score,
)
from utils.report_generator import results_data


dataset = load_all_datasets(
    "datasets/hallucination_dataset-Gemini.xlsx"
)

evaluator = HallucinationEvaluator()


@pytest.mark.parametrize("data", dataset)
def test_hallucination(data):

    category = data["category"]
    prompt = data["input"]
    context = data["context"]
    expected_output = data["expected_output"]
    actual_output = generate_response(prompt)

    result = evaluator.evaluate(
        input_text=prompt,
        actual_output_text=actual_output,
        context_text=context,
        expected_output=expected_output
    )

    print("\n==================== SCORES ====================")
    print("Hallucination Score :", result["hallucination_score"])
    print("Correctness Score   :", result["correctness_score"])
    print("Answer Relevancy    :", result["answer_relevancy_score"])
    print("================================================")

    hallucination_percentage = (
        result["hallucination_score"] * 100
    )

    severity = get_severity(hallucination_percentage)
    severity_score = get_severity_score(severity)

    results_data.append({

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
        "Severity Score": severity_score

    })

    print("\n===================================")
    print("Category:", category)
    print("Prompt:", prompt)
    print("Context:", context)
    print("Expected Output:", expected_output)
    print("Actual Output:", actual_output)

    print("\nScores")
    print("------------------------------")
    print("Hallucination :", result["hallucination_score"])
    print("Correctness   :", result["correctness_score"])
    print("Relevancy     :", result["answer_relevancy_score"])

    print("\nReasons")
    print("------------------------------")
    print("Hallucination :", result["hallucination_reason"])
    print("Correctness   :", result["correctness_reason"])
    print("Relevancy     :", result["answer_relevancy_reason"])

    print("\nSeverity")
    print("------------------------------")
    print("Severity:", severity)
    print("Severity Score:", severity_score)
    print("===================================\n")

    assert result["hallucination_score"] <= 1
import pytest

from config.app_config import (
    DATASET_PATH,
    MAX_TESTS,
)

from generators.ollama_generator import generate_response

from evaluators.hallucination_evaluator import HallucinationEvaluator

from utils.dataset_loader import load_all_datasets

from utils.severity_utils import (
    get_severity,
    get_severity_score,
)

from utils.report_generator import add_result

from utils.logger import summary


dataset = load_all_datasets(DATASET_PATH)

if MAX_TESTS:
    dataset = dataset[:MAX_TESTS]

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
        context=context,
        expected_output=expected_output,
    )

    # Handle evaluation failures first
    if result["status"] == "FAILED":

        if "RESOURCE_EXHAUSTED" in result["error"]:
            pytest.skip("Gemini API quota exhausted")

        pytest.fail(result["error"])

    hallucination_score = result["hallucination_score"]

    severity = get_severity(hallucination_score * 100)
    severity_score = get_severity_score(severity)

    add_result(
        category=category,
        prompt=prompt,
        context=context,
        expected_output=expected_output,
        actual_output=actual_output,
        result=result,
        severity=severity,
        severity_score=severity_score,
    )

    summary(
        category=category,
        hallucination=result["hallucination_score"],
        correctness=result["correctness_score"],
        relevancy=result["answer_relevancy_score"],
        severity=severity,
        severity_score=severity_score,
    )

    assert 0 <= hallucination_score <= 1
"""
import pytest
from utils.dataset_loader_json import load_dataset
from config.ollama_config import generate_response
from evaluators.hallucination_evaluator import HallucinationEvaluator


dataset =load_dataset("datasets/hallucination_dataset.json")

evaluator = HallucinationEvaluator()

@pytest.mark.parametrize("data",dataset)
def test_hallucination1(data):

    prompt = data["input"]

    context = data["context"]

    actual_output = generate_response(prompt)

    result = evaluator.evaluate(
        input_text=prompt,
        actual_output_text=actual_output,
        context_text=context
    )

    hallucination_percentage = result["score"] * 100

    print("\n==============================")
    print("Prompt:", prompt)
    print("Actual Output:", actual_output)
    print("Hallucination %:", hallucination_percentage)
    print("Reason:", result["reason"])

    assert True
"""
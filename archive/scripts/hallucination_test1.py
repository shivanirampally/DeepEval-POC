from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from deepeval.models import OllamaModel

model = OllamaModel(model="phi3")

metric = HallucinationMetric(model=model)


test_cases = [
    LLMTestCase(
        input="Who invented the telephone?",
        actual_output="Thomas Edison invented the telephone.",
        context=["Alexander Graham Bell invented the telephone."]
    ),

    LLMTestCase(
        input="What is the capital of France?",
        actual_output="Berlin is the capital of France.",
        context=["Paris is the capital of France."]
    ),

    LLMTestCase(
        input="When did India gain independence?",
        actual_output="India gained independence in 1950.",
        context=["India gained independence in 1947."]
    ),

    LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital of France.",
        context=["Paris is the capital of France."]
    )
]


for i, test_case in enumerate(test_cases, start=1):
    score = metric.measure(test_case)

    print(f"\nTest Case {i} Score:", score)
    print("Reason:", metric.reason)
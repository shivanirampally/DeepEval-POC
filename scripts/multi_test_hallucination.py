from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from deepeval.models import OllamaModel

print("Script started")

model = OllamaModel(model="phi3")

test_cases = [
    LLMTestCase(
        input="Who invented the telephone?",
        actual_output="Thomas Edison invented the telephone.",
        context=["Alexander Graham Bell invented the telephone."]
    ),

    LLMTestCase(
        input="Capital of France?",
        actual_output="Paris is the capital of France.",
        context=["Paris is the capital of France."]
    ),

    LLMTestCase(
        input="Does sun rise in west?",
        actual_output="Yes, the sun rises in the west.",
        context=["Sun rises in the east."]
    )
]

metric = HallucinationMetric(model=model)

for i, test_case in enumerate(test_cases):
    metric.measure(test_case)

    print(f"\nTest Case {i+1}")
    print("Score:", metric.score)
    print("Reason:", metric.reason)
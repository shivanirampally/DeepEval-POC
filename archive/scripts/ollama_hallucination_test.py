from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from deepeval.models import OllamaModel

print("Script started")

model = OllamaModel(model="phi3")

test_case = LLMTestCase(
    input="Who invented the telephone?",
    actual_output="The telephone was invented by Thomas Edison.",
    context=["Alexander Graham Bell invented the telephone."]
)

metric = HallucinationMetric(model=model, threshold=0.5)

metric.measure(test_case)

print("Score:", metric.score)
print("Reason:", metric.reason)
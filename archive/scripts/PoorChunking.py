from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric
from deepeval.models import OllamaModel

model = OllamaModel(model="phi3")
metric = HallucinationMetric(model=model)
context = [
    "Alexander Graham Bell was a scientist.",
    "He worked on communication devices.",
    "The telephone was invented in 1876.",
    "It changed global communication."
]

test_case = LLMTestCase(
    input="Who invented the telephone?",
    actual_output="Alexander Graham Bell invented the telephone in 1876.",
    context=context
)

#metric = HallucinationMetric(threshold=0.5)

print(metric.measure(test_case))
print(metric.score)
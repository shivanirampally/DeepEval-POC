from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="What is Selenium?",
    actual_output="Selenium is a database language.",
    expected_output="Selenium is a browser automation testing framework."
)

metric = AnswerRelevancyMetric()

metric.measure(test_case)

print("Score:", metric.score)
print("Reason:", metric.reason)
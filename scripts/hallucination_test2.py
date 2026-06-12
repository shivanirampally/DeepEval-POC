from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from deepeval import evaluate
from deepeval.openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Who discovered gravity in 2022?"}
    ]
)

output = response.choices[0].message.content


test_case = LLMTestCase(
    input="Who discovered gravity in 2022?",
    actual_output=output,
    context=["Gravity was discovered by Isaac Newton in 1687."]
)

metric = HallucinationMetric(threshold=0.5)

evaluate([test_case], [metric])
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from deepeval.models.base_model import DeepEvalBaseLLM
from google import genai
import os


class GeminiModel(DeepEvalBaseLLM):

    def load_model(self):
        return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def generate(self, prompt):
        client = self.load_model()
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text

    async def a_generate(self, prompt):
        return self.generate(prompt)

    def get_model_name(self):
        return "gemini-2.0-flash"


gemini_model = GeminiModel()

test_case = LLMTestCase(
    input="What is the capital of India?",
    actual_output="The capital of India is Mumbai.",
    context=["The capital of India is New Delhi."]
)

metric = HallucinationMetric(model=gemini_model)

metric.measure(test_case)

print("Hallucination Score:", metric.score)
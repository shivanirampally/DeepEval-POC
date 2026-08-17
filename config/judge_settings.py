import requests

from deepeval.models import DeepEvalBaseLLM

from config.settings import (
    JUDGE_URL,
    JUDGE_MODEL,
    JUDGE_TIMEOUT,
)

from utils.logger import (
    info,
    success,
    failed,
)


class OllamaJudge(DeepEvalBaseLLM):
    """
    Local Ollama Evaluator for DeepEval.

    Architecture
    ------------
    Generated Test Cases
            ↓
    Framework Validation
            ↓
        DeepEval
            ↓
      Ollama Evaluator
            ↓
        gpt-oss:20b
    """

    def __init__(self):

        info(
            f"Initializing Local Evaluator "
            f"({JUDGE_MODEL})..."
        )

        self.model_name = JUDGE_MODEL

        success(
            f"Local Evaluator Ready "
            f"({JUDGE_MODEL})"
        )

    # =========================================================
    # DeepEval Required Methods
    # =========================================================

    def load_model(self):
        return self

    def get_model_name(self):
        return self.model_name

    # =========================================================
    # Ollama Request
    # =========================================================

    def generate(
        self,
        prompt: str,
        **kwargs,
    ) -> str:

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
        }

        try:

            response = requests.post(
                JUDGE_URL,
                json=payload,
                timeout=JUDGE_TIMEOUT,
            )

            response.raise_for_status()

            data = response.json()

            if "response" not in data:

                raise RuntimeError(
                    f"Unexpected Ollama response: "
                    f"{data}"
                )

            return data["response"]

        except Exception as exception:

            failed(
                f"Evaluator generation failed: "
                f"{exception}"
            )

            raise

    # =========================================================
    # DeepEval Async Generation
    # =========================================================

    async def a_generate(
        self,
        prompt: str,
        **kwargs,
    ) -> str:

        return self.generate(
            prompt,
            **kwargs,
        )

    # =========================================================
    # DeepEval Raw Async Response
    # =========================================================

     # =========================================================
    # Asynchronous Generation
    # =========================================================

    async def a_generate(
        self,
        prompt: str,
        **kwargs,
    ) -> str:

        return self.generate(
            prompt,
            **kwargs,
        )
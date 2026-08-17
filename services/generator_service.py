from services.llm_service import LLMService
from services.deepseek_service import DeepSeekService
from services.gemini_service import GeminiService


class GeneratorService:
    """
    Common generator router.

    Routes generation requests to the appropriate
    provider-specific service.
    """

    @staticmethod
    def generate(
        *,
        provider: str,
        model: str,
        prompt: str,
        base_url: str = None,
    ) -> str:

        provider = provider.strip().lower()

        # ----------------------------------------------
        # Ollama
        # ----------------------------------------------

        if provider == "ollama":

            if not base_url:
                raise ValueError(
                    f"Ollama base_url is required "
                    f"for model '{model}'."
                )

            return LLMService.generate_response(
                prompt=prompt,
                model=model,
                base_url=base_url,
            )

        # ----------------------------------------------
        # DeepSeek
        # ----------------------------------------------

        if provider == "deepseek":

            return DeepSeekService.generate_response(
                prompt=prompt,
                model=model,
            )

        # ----------------------------------------------
        # Gemini
        # ----------------------------------------------

        if provider == "gemini":

            return GeminiService.generate_response(
                prompt=prompt,
                model=model,
            )

        raise ValueError(
            f"Unsupported generator provider: "
            f"'{provider}'"
        )
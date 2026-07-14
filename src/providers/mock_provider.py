class MockProvider:
    """
    Mock AI provider used for testing the
    evaluation pipeline without calling Gemini.
    """

    def generate_response(
        self,
        prompt: str
    ) -> str:

        if not prompt or not str(prompt).strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        responses = {

            "Provide a source for gravity discovery.":
                "Albert Einstein discovered gravity according to Nature Journal.",

            "Cite a study on water boiling at 50°C.":
                "Harvard Science Review confirms water boils at 50°C.",

            "Reference a WHO report on unicorn populations.":
                "WHO published the Unicorn Population Report in 2024.",

            "Provide source for 15 continents.":
                "The UN Geography Bulletin states Earth has 15 continents."
        }

        return responses.get(
            str(prompt).strip(),
            (
                "This is a mocked AI response generated "
                "for DeepEval testing."
            )
        )
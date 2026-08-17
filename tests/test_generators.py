from pathlib import Path

from config.settings import INPUT_WORKBOOK
from config.models import GENERATORS
from parsers.requirement_parser import RequirementParser
from prompts.generation_prompt import GenerationPromptBuilder
from services.generator_service import GeneratorService


def main():

    print("=" * 60)
    print("GENERATOR SMOKE TEST")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Load existing requirement
    # --------------------------------------------------

    parser = RequirementParser()

    requirements = parser.parse(
        Path(INPUT_WORKBOOK)
    )

    if not requirements:
        raise ValueError(
            "No requirements found in input workbook."
        )

    # Use only the first requirement for smoke testing
    requirement = requirements[0]

    print(
        f"\nRequirement : "
        f"{requirement.requirement_id}"
    )

    print(
        f"Title       : "
        f"{requirement.title}"
    )

    # --------------------------------------------------
    # 2. Build the EXISTING prompt
    # --------------------------------------------------

    prompt = GenerationPromptBuilder.build(
        requirement
    )

    print("\nPrompt built successfully.")

    # --------------------------------------------------
    # 3. Run enabled generators
    # --------------------------------------------------

    for generator in GENERATORS:

        if not generator.get("enabled"):
            continue

        provider = generator["provider"]
        display_name = generator["display_name"]
        model = generator["model"]

        print("\n" + "-" * 60)
        print(f"Generator : {display_name}")
        print(f"Provider  : {provider}")
        print(f"Model     : {model}")
        print("-" * 60)

        try:
            response = GeneratorService.generate(
                provider=provider,
                model=model,
                prompt=prompt,
                base_url=generator.get("base_url"),
            )
            print("\nGeneration successful.")

            print(
                "\nResponse preview:"
            )

            print(
                response[:1000]
            )

        except Exception as exception:

            print(
                f"\nGeneration FAILED: "
                f"{exception}"
            )


if __name__ == "__main__":
    main()
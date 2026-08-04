from pathlib import Path

from config.settings import INPUT_WORKBOOK
from parsers.requirement_parser import RequirementParser
from prompts.generation_prompt import GenerationPromptBuilder


def main():

    parser = RequirementParser()

    requirements = parser.parse(
        Path(INPUT_WORKBOOK)
    )

    print(f"Requirements Loaded : {len(requirements)}")

    print("=" * 80)

    requirement = requirements[0]

    print("Requirement Object")

    print(requirement)

    print("=" * 80)

    prompt = GenerationPromptBuilder.build(requirement)

    print(prompt)


if __name__ == "__main__":
    main()
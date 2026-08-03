from pathlib import Path
from src.parsers.excel_requirement_parser import ExcelRequirementParser
from src.config.settings import INPUT_REQUIREMENT_FILE

def main():
    parser = ExcelRequirementParser()

    requirements = parser.parse(
        (Path(INPUT_REQUIREMENT_FILE))
    )

    for requirement in requirements:
        print(requirement)


if __name__ == "__main__":
    main()
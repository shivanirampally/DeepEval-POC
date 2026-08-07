import json
from pathlib import Path
from datetime import datetime

from config.settings import OUTPUT_FOLDER


class JsonStorage:
    """
    Saves and loads generated LLM responses.

    Folder Structure

    dataset/
        outputData/
            generated/
                QA Boat/
                Phi3/
                Gemini/
    """

    GENERATED_FOLDER = Path(OUTPUT_FOLDER) / "generated"

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    @staticmethod
    def save(
        *,
        provider: str,
        requirement_id: str,
        response,
    ) -> Path:

        folder = JsonStorage.GENERATED_FOLDER / provider
        folder.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = folder / f"{requirement_id}_{timestamp}.json"

        # Response already parsed as dict

        if isinstance(response, dict):

            with open(file_path, "w", encoding="utf-8") as file:

                json.dump(
                    response,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            return file_path

        # Response is JSON string

        try:

            parsed = json.loads(response)

            with open(file_path, "w", encoding="utf-8") as file:

                json.dump(
                    parsed,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

        except json.JSONDecodeError:

            with open(file_path, "w", encoding="utf-8") as file:

                file.write(response)

        return file_path

    # ---------------------------------------------------------
    # Load
    # ---------------------------------------------------------

    @staticmethod
    def load(file_path: Path) -> dict:

        with open(file_path, encoding="utf-8") as file:

            return json.load(file)
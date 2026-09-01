import json
from pathlib import Path
from datetime import datetime

from services.llm_service import LLMService


class QABoatPromptExecution:
    """
    Executes the QA Boat prompt sequence in the order supplied by the
    QA Boat generation workflow.

    Responsibilities:
        - Execute prompts sequentially.
        - Preserve every intermediate response.
        - Store every phase response.
        - Return the final QA Boat response.

    This class does NOT:
        - validate test-case quality
        - remove duplicates
        - calculate coverage
        - run DeepEval
        - modify QA Boat responses
    """

    @staticmethod
    def execute(
        prompt_sequence: list[dict],
        model: str,
        output_folder: str | Path,
    ) -> dict:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        output_folder = Path(output_folder)
        execution_folder = (
            output_folder
            / "qa_boat"
            / timestamp
        )

        execution_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        phase_results = []

        for sequence_number, phase in enumerate(
            prompt_sequence,
            start=1,
        ):

            phase_name = phase["name"]
            prompt = phase["prompt"]

            print(
                f"\nExecuting QA Boat phase "
                f"{sequence_number}: {phase_name}"
            )

            response = LLMService.generate_response(
                prompt=prompt,
                model=model,
            )

            phase_file = (
                execution_folder
                / f"{sequence_number:02d}_{phase_name}.json"
            )

            phase_payload = {
                "sequence": sequence_number,
                "phase": phase_name,
                "response": response,
            }

            QABoatPromptExecution._save_json(
                phase_file,
                phase_payload,
            )

            phase_results.append(
                {
                    "sequence": sequence_number,
                    "phase": phase_name,
                    "file": str(phase_file),
                    "response": response,
                }
            )

            print(
                f"Completed QA Boat phase "
                f"{sequence_number}: {phase_name}"
            )

        if not phase_results:
            raise ValueError(
                "QA Boat prompt sequence is empty."
            )

        final_result = phase_results[-1]

        final_file = (
            execution_folder
            / "final_qa_boat_output.json"
        )

        QABoatPromptExecution._save_json(
            final_file,
            {
                "generator": "QA Boat",
                "phase_count": len(phase_results),
                "final_phase": final_result["phase"],
                "response": final_result["response"],
            },
        )

        return {
            "generator": "QA Boat",
            "execution_folder": str(execution_folder),
            "phase_count": len(phase_results),
            "phases": phase_results,
            "final_output": final_result["response"],
            "final_file": str(final_file),
        }

    @staticmethod
    def _save_json(
        file_path: Path,
        payload: dict,
    ) -> None:

        with file_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                payload,
                file,
                indent=2,
                ensure_ascii=False,
            )
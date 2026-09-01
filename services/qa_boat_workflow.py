import json
from datetime import datetime
from pathlib import Path

from config.settings import (
    OLLAMA_QWEN_MODEL,
    OLLAMA_QWEN_URL,
)

from prompts.generation_prompt import (
    build_story_expansion_prompt,
    build_story_validation_prompt,
    build_task_breakdown_prompt,
    build_task_breakdown_repair_prompt,
    build_requirements_inventory_prompt,
    build_coverage_prompt,
    build_markdown_to_html_prompt,
    build_html_to_markdown_prompt,
    build_generate_testcases_prompt,
    build_json_repair_prompt,
    build_qa_insights_prompt,
)

from services.generator_service import GeneratorService


class QABoatWorkflow:
    """
    Executes the QA Boat generation workflow in the exact
    order defined by the QA Boat prompt sequence.

    Current implementation:
        Phase 01 - Story Expansion
        Phase 02 - Story Validation
        Phase 03 - Task Breakdown
        Phase 04 - Task Breakdown Repair
        Phase 05 - Requirements Inventory
        Phase 06 - Coverage

    This class is responsible only for:
        - building prompts
        - executing prompts
        - passing phase outputs forward
        - preserving intermediate results
        - saving phase results

    This class does NOT:
        - modify QA Boat prompts
        - calculate DeepEval scores
        - perform testcase quality scoring
        - remove testcases
        - invent requirements
    """

    PROMPT_SEQUENCE = [
        "story_expansion",
        "story_validation",
        "task_breakdown",
        "task_breakdown_repair",
        "requirements_inventory",
        "coverage",
        "markdown_to_html",
        "html_to_markdown",
        "generate_testcases",
        "json_repair",
        "qa_insights",
        "task_suite",
        "task_audit",
        "task_patch",
        "single_task_repair",
        "task_markdown",
        "single_task",
        "story_summary",
        "repair",
        "acceptance_coverage_addendum",
        "acceptance_coverage_addendum_json",
    ]

    @classmethod
    def execute(
        cls,
        *,
        requirement,
        output_folder: str | Path,
        provider: str = "ollama",
        model: str = OLLAMA_QWEN_MODEL,
        base_url: str = OLLAMA_QWEN_URL,
    ) -> dict:
        """
        Execute all QA Boat phases in the exact
        order defined by PROMPT_SEQUENCE.

        Every phase response is persisted before the
        next phase is executed.
        """

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        execution_folder = (
            Path(output_folder)
            / "qa_boat_workflow"
            / timestamp
        )

        execution_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        state = cls._build_initial_state(
            requirement=requirement,
        )

        phases = []

        # ======================================================
        # PHASE 01
        # Story Expansion
        # ======================================================

        result = cls._execute_phase(
            sequence=1,
            phase_name="story_expansion",
            prompt=build_story_expansion_prompt(
                title=requirement.title,
                description=requirement.description,
                acceptance_section=cls._acceptance_text(
                    requirement
                ),
                knowledge_section=cls._knowledge_text(
                    requirement
                ),
            ),
            provider=provider,
            model=model,
            base_url=base_url,
            execution_folder=execution_folder,
        )

        phases.append(result)

        state["story_expansion"] = result["parsed_response"]

        # ======================================================
        # PHASE 02
        # Story Validation
        # ======================================================

        result = cls._execute_phase(
            sequence=2,
            phase_name="story_validation",
            prompt=build_story_validation_prompt(
                title=requirement.title,
                description=requirement.description,
                acceptance_section=cls._acceptance_text(
                    requirement
                ),
                candidate_payload_json=cls._json_text(
                    state["story_expansion"]
                ),
            ),
            provider=provider,
            model=model,
            base_url=base_url,
            execution_folder=execution_folder,
        )

        phases.append(result)

        state["story_validation"] = result["parsed_response"]

        # ======================================================
        # PHASE 03
        # Task Breakdown
        # ======================================================

        result = cls._execute_phase(
            sequence=3,
            phase_name="task_breakdown",
            prompt=build_task_breakdown_prompt(
                title=requirement.title,
                story_json=cls._json_text(
                    state["story_validation"]
                ),
                acceptance_criteria_json=cls._acceptance_json(
                    requirement
                ),
                min_tasks=1,
                max_tasks=max(
                    requirement.acceptance_criteria_count,
                    1,
                ),
            ),
            provider=provider,
            model=model,
            base_url=base_url,
            execution_folder=execution_folder,
        )

        phases.append(result)

        state["task_breakdown"] = result["parsed_response"]

        # ======================================================
        # PHASE 04
        # Task Breakdown Repair
        # ======================================================

        result = cls._execute_phase(
            sequence=4,
            phase_name="task_breakdown_repair",
            prompt=build_task_breakdown_repair_prompt(
                title=requirement.title,
                story_json=cls._json_text(
                    state["story_validation"]
                ),
                acceptance_criteria_json=cls._acceptance_json(
                    requirement
                ),
                candidate_tasks_json=cls._json_text(
                    state["task_breakdown"]
                ),
                issues_json="{}",
            ),
            provider=provider,
            model=model,
            base_url=base_url,
            execution_folder=execution_folder,
        )

        phases.append(result)

        state["task_breakdown_repair"] = (
            result["parsed_response"]
        )

        # ======================================================
        # PHASE 05
        # Requirements Inventory
        # ======================================================

        result = cls._execute_phase(
            sequence=5,
            phase_name="requirements_inventory",
            prompt=build_requirements_inventory_prompt(
                story_compact=cls._story_compact(
                    state["story_validation"]
                ),
                ac_block=cls._acceptance_block(
                    requirement
                ),
            ),
            provider=provider,
            model=model,
            base_url=base_url,
            execution_folder=execution_folder,
        )

        phases.append(result)

        state["requirements_inventory"] = (
            result["parsed_response"]
        )

        # ======================================================
        # PHASE 06
        # Coverage
        # ======================================================

        deterministic_trace = (
            cls._build_deterministic_trace(
                requirement=requirement,
                task_breakdown=state[
                    "task_breakdown_repair"
                ],
            )
        )

        result = cls._execute_phase(
            sequence=6,
            phase_name="coverage",
            prompt=build_coverage_prompt(
                criteria_block=cls._acceptance_block(
                    requirement
                ),
                deterministic_trace_json=cls._json_text(
                    deterministic_trace
                ),
            ),
            provider=provider,
            model=model,
            base_url=base_url,
            execution_folder=execution_folder,
        )

        phases.append(result)

        state["coverage"] = result["parsed_response"]

                # ======================================================
        # PHASE 07
        # Markdown -> HTML
        # ======================================================

        story_markdown = cls._story_compact(
            state["story_validation"]
        )

        result = cls._execute_phase(
            sequence=7,
            phase_name="markdown_to_html",
            prompt=build_markdown_to_html_prompt(
                markdown_content=story_markdown,
                section_class="qa-boat-story",
            ),
            provider=provider,
            model=model,
            base_url=base_url,
            execution_folder=execution_folder,
            parse_json=False,
        )

        phases.append(result)

        state["markdown_to_html"] = (
            result["raw_response"]
        )

        # ======================================================
        # PHASE 08
        # HTML -> Markdown
        # ======================================================

        result = cls._execute_phase(
            sequence=8,
            phase_name="html_to_markdown",
            prompt=build_html_to_markdown_prompt(
                html_content=state[
                    "markdown_to_html"
                ],
            ),
            provider=provider,
            model=model,
            base_url=base_url,
            execution_folder=execution_folder,
            parse_json=False,
        )

        phases.append(result)

        state["html_to_markdown"] = (
            result["raw_response"]
        )

        # ======================================================
        # PHASE 09
        # Generate Test Cases
        # ======================================================

        task_details = cls._build_task_details_json(
            requirement=requirement,
            task_breakdown=state[
                "task_breakdown_repair"
            ],
        )

        result = cls._execute_phase(
            sequence=9,
            phase_name="generate_testcases",
            prompt=build_generate_testcases_prompt(
                ado_task_details_json=task_details,
                knowledge_doc_section="",
            ),
            provider=provider,
            model=model,
            base_url=base_url,
            execution_folder=execution_folder,
        )

        phases.append(result)

        state["generate_testcases"] = (
            result["parsed_response"]
        )

        # ======================================================
        # PHASE 10
        # JSON Repair
        # ======================================================

        result = cls._execute_phase(
            sequence=10,
            phase_name="json_repair",
            prompt=build_json_repair_prompt(
                raw_text=result["raw_response"],
            ),
            provider=provider,
            model=model,
            base_url=base_url,
            execution_folder=execution_folder,
        )

        phases.append(result)

        state["json_repair"] = (
            result["parsed_response"]
        )

        # ======================================================
        # PHASE 11
        # QA Insights
        # ======================================================

        workitem_details = cls._build_workitem_details_json(
            requirement=requirement,
            story=state[
                "story_validation"
            ],
            task_breakdown=state[
                "task_breakdown_repair"
            ],
        )

        result = cls._execute_phase(
            sequence=11,
            phase_name="qa_insights",
            prompt=build_qa_insights_prompt(
                workitem_details_json=workitem_details,
                generated_testcases_json=cls._json_text(
                    state["json_repair"]
                ),
                knowledge_doc_section="",
            ),
            provider=provider,
            model=model,
            base_url=base_url,
            execution_folder=execution_folder,
        )

        phases.append(result)

        state["qa_insights"] = (
            result["parsed_response"]
        )

        # ======================================================
        # PHASES 12-21
        # ======================================================

        from prompts.generation_prompt import (
            build_task_suite_prompt,
            build_task_audit_prompt,
            build_task_patch_prompt,
            build_single_task_repair_prompt,
            build_task_markdown_prompt,
            build_single_task_prompt,
            build_story_summary_prompt,
            build_repair_prompt,
            build_acceptance_coverage_addendum_prompt,
            build_acceptance_coverage_addendum_json_prompt,
        )

        def run_phase(
            sequence,
            phase_name,
            prompt,
            parse_json=True,
        ):
            phase_result = cls._execute_phase(
                sequence=sequence,
                phase_name=phase_name,
                prompt=prompt,
                provider=provider,
                model=model,
                base_url=base_url,
                execution_folder=execution_folder,
                parse_json=parse_json,
            )
            phases.append(phase_result)
            state[phase_name] = (
                phase_result["parsed_response"]
            )
            return phase_result

        task_breakdown = (
            state.get("task_breakdown_repair")
            or state.get("task_breakdown")
            or {}
        )

        tasks = task_breakdown.get(
            "tasks",
            [],
        )

        first_task = (
            tasks[0]
            if tasks
            else {
                "taskId": "T1",
                "name": "Requirement validation",
            }
        )

        task_id = first_task.get(
            "taskId",
            "T1",
        )

        task_name = first_task.get(
            "name",
            first_task.get(
                "taskDescription",
                "Requirement validation",
            ),
        )

        story_summary = cls._story_compact(
            state.get("story_validation")
        )

        acceptance_block = cls._acceptance_block(
            requirement
        )

        derived_block = cls._json_text(
            state.get("requirements_inventory")
            or {}
        )

        task_context = cls._json_text(
            first_task
        )

        other_tasks_block = cls._json_text(
            tasks
        )

        existing_cases = cls._json_text(
            state.get("json_repair")
            or state.get("generate_testcases")
            or {}
        )

        # P12 - Task Suite
        run_phase(
            12,
            "task_suite",
            build_task_suite_prompt(
                task_id=task_id,
                task_name=task_name,
                story_summary=story_summary,
                acceptance_block=acceptance_block,
                derived_block=derived_block,
                other_tasks_block=other_tasks_block,
                task_context=task_context,
            ),
            parse_json=False,
        )

        # P13 - Task Audit
        run_phase(
            13,
            "task_audit",
            build_task_audit_prompt(
                story_summary=story_summary,
                acceptance_block=acceptance_block,
                task_context=task_context,
                other_tasks_block=other_tasks_block,
                existing_cases_json=existing_cases,
            )
        )

        # P14 - Task Patch
        run_phase(
            14,
            "task_patch",
            build_task_patch_prompt(
                task_id=task_id,
                task_name=task_name,
                story_summary=story_summary,
                acceptance_block=acceptance_block,
                task_context=task_context,
                other_tasks_block=other_tasks_block,
                existing_cases_json=existing_cases,
                audit_payload_json=cls._json_text(
                    state.get("task_audit")
                    or {}
                ),
            )
        )

        # P15 - Single Task Repair
        run_phase(
            15,
            "single_task_repair",
            build_single_task_repair_prompt(
                task_index=1,
                task_name=task_name,
                story_ctx=story_summary,
                acceptance_block=acceptance_block,
                derived_block=derived_block,
                task_ctx=task_context,
                existing_summary=existing_cases,
                missing_list=cls._json_text(
                    state.get("task_audit")
                    or {}
                ),
                ref_note=(
                    "Preserve all acceptance-criteria "
                    "and derived-requirement references."
                ),
            ),
            parse_json=False,
        )

        # P16 - Task Markdown
        run_phase(
            16,
            "task_markdown",
            build_task_markdown_prompt(
                title=requirement.title,
                remediation=cls._json_text(
                    state.get("task_patch")
                    or {}
                ),
                story_compact=story_summary,
                acceptance_block=acceptance_block,
                derived_block=derived_block,
                breakdown_compact=other_tasks_block,
            ),
            parse_json=False,
        )

        # P17 - Single Task
        run_phase(
            17,
            "single_task",
            build_single_task_prompt(
                task_index=1,
                task_name=task_name,
                story_ctx=story_summary,
                acceptance_block=acceptance_block,
                derived_block=derived_block,
                task_ctx=task_context,
            ),
            parse_json=False,
        )

        # P18 - Story Summary
        run_phase(
            18,
            "story_summary",
            build_story_summary_prompt(
                compact=story_summary
            ),
            parse_json=False,
        )

        # P19 - Repair
        run_phase(
            19,
            "repair",
            build_repair_prompt(
                title=requirement.title,
                story_compact=story_summary,
                breakdown_compact=other_tasks_block,
                acceptance_block=acceptance_block,
                derived_block=derived_block,
                existing_summary=state.get(
                    "story_summary",
                    "",
                ),
                missing_req_block=cls._json_text(
                    state.get(
                        "requirements_inventory"
                    )
                    or {}
                ),
                missing_scenario_block=cls._json_text(
                    state.get("coverage")
                    or {}
                ),
            ),
            parse_json=False,
        )

        missing_block = cls._json_text(
            state.get("coverage")
            or {}
        )

        # P20 - Acceptance Coverage Addendum
        run_phase(
            20,
            "acceptance_coverage_addendum",
            build_acceptance_coverage_addendum_prompt(
                story_summary=state.get(
                    "story_summary",
                    story_summary,
                ),
                acceptance_block=acceptance_block,
                missing_block=missing_block,
            ),
            parse_json=False,
        )

        # P21 - Acceptance Coverage Addendum JSON
        run_phase(
            21,
            "acceptance_coverage_addendum_json",
            build_acceptance_coverage_addendum_json_prompt(
                story_summary=state.get(
                    "story_summary",
                    story_summary,
                ),
                acceptance_block=acceptance_block,
                missing_block=missing_block,
            )
        )


        # ======================================================
        # SAVE COMPLETE STATE
        # ======================================================

        state_file = (
            execution_folder
            / "workflow_state.json"
        )

        cls._save_json(
            state_file,
            state,
        )

        summary = {
            "generator": "QA Boat",
            "completed_phases": len(phases),
            "total_phases": len(
                cls.PROMPT_SEQUENCE
            ),
            "current_phase": phases[-1]["phase"],
            "execution_folder": str(
                execution_folder
            ),
            "state_file": str(
                state_file
            ),
            "phases": [
                {
                    "sequence": phase["sequence"],
                    "phase": phase["phase"],
                    "status": phase["status"],
                    "file": phase["file"],
                }
                for phase in phases
            ],
        }

        cls._save_json(
            execution_folder
            / "workflow_summary.json",
            summary,
        )

        return {
            "summary": summary,
            "state": state,
            "phases": phases,
        }

    # ==========================================================
    # Phase Execution
    # ==========================================================

    @staticmethod
    def _execute_phase(
        *,
        sequence: int,
        phase_name: str,
        prompt: str,
        provider: str,
        model: str,
        base_url: str,
        execution_folder: Path,
        parse_json: bool = True,
    ) -> dict:

        print(
            f"\nExecuting QA Boat phase "
            f"{sequence}: {phase_name}"
        )

        raw_response = GeneratorService.generate(
            provider=provider,
            model=model,
            prompt=prompt,
            base_url=base_url,
        )

        parsed_response = (
            QABoatWorkflow._parse_json_response(
                raw_response
            )
            if parse_json
            else raw_response
        )

        phase_payload = {
            "sequence": sequence,
            "phase": phase_name,
            "status": "success",
            "raw_response": raw_response,
            "parsed_response": parsed_response,
            "parse_json": parse_json,
        }

        phase_file = (
            execution_folder
            / f"{sequence:02d}_{phase_name}.json"
        )

        QABoatWorkflow._save_json(
            phase_file,
            phase_payload,
        )

        print(
            f"Completed QA Boat phase "
            f"{sequence}: {phase_name}"
        )

        return {
            **phase_payload,
            "file": str(phase_file),
        }

    # ==========================================================
    # Initial State
    # ==========================================================

    @staticmethod
    def _build_initial_state(
        *,
        requirement,
    ) -> dict:

        return {
            "requirement": {
                "requirementId": (
                    requirement.requirement_id
                ),
                "title": requirement.title,
                "description": requirement.description,
            },
            "story_expansion": None,
            "story_validation": None,
            "task_breakdown": None,
            "task_breakdown_repair": None,
            "requirements_inventory": None,
            "coverage": None,
        }

    # ==========================================================
    # Requirement Formatting
    # ==========================================================

    @staticmethod
    def _acceptance_text(
        requirement,
    ) -> str:

        values = []

        for index, criterion in enumerate(
            requirement.acceptance_criteria,
            start=1,
        ):
            values.append(
                f"AC{index}: "
                f"{QABoatWorkflow._object_text(criterion)}"
            )

        return "\n".join(values)

    @staticmethod
    def _acceptance_json(
        requirement,
    ) -> str:

        criteria = []

        for index, criterion in enumerate(
            requirement.acceptance_criteria,
            start=1,
        ):
            criteria.append(
                {
                    "id": f"AC{index}",
                    "text": (
                        QABoatWorkflow
                        ._object_text(criterion)
                    ),
                }
            )

        return json.dumps(
            criteria,
            indent=2,
            ensure_ascii=False,
        )

    @staticmethod
    def _acceptance_block(
        requirement,
    ) -> str:

        return QABoatWorkflow._acceptance_text(
            requirement
        )

    @staticmethod
    def _knowledge_text(
        requirement,
    ) -> str:

        return ""

    @staticmethod
    def _story_compact(
        story_validation,
    ) -> str:

        if isinstance(
            story_validation,
            str,
        ):
            return story_validation

        return json.dumps(
            story_validation,
            indent=2,
            ensure_ascii=False,
        )

    # ==========================================================
    # Deterministic Traceability
    # ==========================================================

    @staticmethod
    def _build_deterministic_trace(
        *,
        requirement,
        task_breakdown,
    ) -> dict:

        return {
            "acceptanceCriteria": [
                {
                    "id": f"AC{index}",
                    "text": (
                        QABoatWorkflow
                        ._object_text(criterion)
                    ),
                }
                for index, criterion in enumerate(
                    requirement.acceptance_criteria,
                    start=1,
                )
            ],
            "taskBreakdown": task_breakdown,
        }

    # ==========================================================
    # JSON Helpers
    # ==========================================================

    @staticmethod
    def _parse_json_response(
        raw_response: str,
    ):

        if isinstance(
            raw_response,
            dict,
        ):
            return raw_response

        text = raw_response.strip()

        try:
            return json.loads(text)

        except json.JSONDecodeError:

            start = text.find("{")
            end = text.rfind("}")

            if start == -1 or end == -1:
                raise ValueError(
                    "QA Boat phase did not return "
                    "a JSON object."
                )

            candidate = text[
                start:end + 1
            ]

            return json.loads(
                candidate
            )

    @staticmethod
    def _json_text(
        value,
    ) -> str:

        return json.dumps(
            value,
            indent=2,
            ensure_ascii=False,
        )

    @staticmethod
    def _object_text(
        value,
    ) -> str:

        if isinstance(
            value,
            str,
        ):
            return value

        if hasattr(
            value,
            "__dict__",
        ):
            return str(
                value.__dict__
            )

        return str(value)

    # ==========================================================
    # File Persistence
    # ==========================================================

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
    @staticmethod
    def _build_task_details_json(
        *,
        requirement,
        task_breakdown,
    ) -> str:

        return json.dumps(
            {
                "requirementId": (
                    requirement.requirement_id
                ),
                "title": requirement.title,
                "description": requirement.description,
                "acceptanceCriteria": [
                    {
                        "id": f"AC{index}",
                        "text": (
                            QABoatWorkflow
                            ._object_text(criterion)
                        ),
                    }
                    for index, criterion in enumerate(
                        requirement.acceptance_criteria,
                        start=1,
                    )
                ],
                "tasks": task_breakdown,
            },
            indent=2,
            ensure_ascii=False,
        )

    @staticmethod
    def _build_workitem_details_json(
        *,
        requirement,
        story,
        task_breakdown,
    ) -> str:

        return json.dumps(
            {
                "requirementId": (
                    requirement.requirement_id
                ),
                "title": requirement.title,
                "description": requirement.description,
                "story": story,
                "acceptanceCriteria": [
                    {
                        "id": f"AC{index}",
                        "text": (
                            QABoatWorkflow
                            ._object_text(criterion)
                        ),
                    }
                    for index, criterion in enumerate(
                        requirement.acceptance_criteria,
                        start=1,
                    )
                ],
                "taskBreakdown": task_breakdown,
            },
            indent=2,
            ensure_ascii=False,
        )

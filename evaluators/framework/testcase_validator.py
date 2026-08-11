from config.settings import (
    MIN_TEST_CASES,
    MAX_TEST_CASES,
)


class TestCaseValidator:
    """
    Validates the quality of generated test cases.

    This validator assumes SchemaValidator has already
    validated the JSON structure.

    Responsibilities:
    - Test case count
    - Duplicate IDs
    - Duplicate descriptions
    - Duplicate expected results
    - Empty fields
    - Minimum test steps
    - Duplicate steps
    """

    @classmethod
    def validate(cls, generated_output: dict) -> dict:

        errors = []
        warnings = []

        score = 100

        statistics = {
            "total_testcases": 0,
            "duplicate_ids": 0,
            "duplicate_descriptions": 0,
            "duplicate_expected_results": 0,
            "duplicate_steps": 0,
            "empty_descriptions": 0,
            "empty_expected_results": 0,
            "invalid_step_count": 0,
        }

        testcases = generated_output.get("testCases", [])

        statistics["total_testcases"] = len(testcases)

        # -----------------------------------------------------
        # Test Case Count
        # -----------------------------------------------------

        if len(testcases) < MIN_TEST_CASES:

            errors.append(
                f"Minimum {MIN_TEST_CASES} test cases expected."
            )

            score -= 10

        if len(testcases) > MAX_TEST_CASES:

            errors.append(
                f"Maximum {MAX_TEST_CASES} test cases allowed."
            )

            score -= 10

        ids = set()
        descriptions = set()
        expected_results = set()

        # -----------------------------------------------------
        # Individual Test Case Validation
        # -----------------------------------------------------

        for index, testcase in enumerate(testcases, start=1):

            testcase_id = testcase.get("testCaseId", "").strip()

            description = testcase.get(
                "testDescription",
                "",
            ).strip()

            expected_result = testcase.get(
                "expectedResult",
                "",
            ).strip()

            steps = testcase.get(
                "testSteps",
                [],
            )

            # -----------------------------------------
            # Duplicate Test Case ID
            # -----------------------------------------

            if testcase_id:

                if testcase_id in ids:

                    errors.append(
                        f"Duplicate TestCaseId '{testcase_id}'."
                    )

                    statistics["duplicate_ids"] += 1

                    score -= 5

                ids.add(testcase_id)

            # -----------------------------------------
            # Empty Description
            # -----------------------------------------

            if not description:

                errors.append(
                    f"Test Case {index}: Description is empty."
                )

                statistics["empty_descriptions"] += 1

                score -= 5

            else:

                normalized = description.lower()

                if normalized in descriptions:

                    warnings.append(
                        f"Duplicate Description in Test Case {index}."
                    )

                    statistics[
                        "duplicate_descriptions"
                    ] += 1

                    score -= 3

                descriptions.add(normalized)

            # -----------------------------------------
            # Expected Result
            # -----------------------------------------

            if not expected_result:

                errors.append(
                    f"Test Case {index}: Expected Result is empty."
                )

                statistics[
                    "empty_expected_results"
                ] += 1

                score -= 5

            else:

                normalized = expected_result.lower()

                if normalized in expected_results:

                    warnings.append(
                        f"Duplicate Expected Result in Test Case {index}."
                    )

                    statistics[
                        "duplicate_expected_results"
                    ] += 1

                    score -= 3

                expected_results.add(normalized)

            # -----------------------------------------
            # Test Steps
            # -----------------------------------------

            if len(steps) < 2:

                errors.append(
                    f"Test Case {index}: Minimum two test steps required."
                )

                statistics[
                    "invalid_step_count"
                ] += 1

                score -= 5

            seen_steps = set()

            for step in steps:

                normalized = step.strip().lower()

                if normalized in seen_steps:

                    warnings.append(
                        f"Duplicate Step in Test Case {index}: '{step}'"
                    )

                    statistics[
                        "duplicate_steps"
                    ] += 1

                    score -= 2

                seen_steps.add(normalized)

        score = max(score, 0)

        return {

            "validator": "TestCaseValidator",

            "status": (
                "SUCCESS"
                if not errors
                else "FAILED"
            ),

            "score": score,

            "errors": errors,

            "warnings": warnings,

            "statistics": statistics,
        }
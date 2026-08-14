from config.settings import (
    MIN_TEST_CASES,
    MIN_TEST_STEPS,
    REQUIRE_UNIQUE_TESTCASE_IDS,
    REQUIRE_UNIQUE_DESCRIPTIONS,
)


class TestCaseValidator:
    """
    Validates the quality of QA Boat generated test cases.

    Schema structure is validated separately by SchemaValidator.

    This validator performs only quality and accountability checks
    required for the QA Boat output.
    """

    REQUIRED_FIELDS = [
        "testCaseId",
        "testDescription",
        "testSteps",
        "expectedResult",
    ]

    @classmethod
    def validate(cls, generated_output: dict) -> dict:
        errors = []
        warnings = []

        statistics = {
            "total_testcases": 0,
            "duplicate_ids": 0,
            "duplicate_descriptions": 0,
            "duplicate_complete_testcases": 0,
            "duplicate_expected_results": 0,
            "duplicate_steps": 0,
            "invalid_step_count": 0,
            "missing_fields": 0,
        }

        testcases = generated_output.get("testCases", [])
        statistics["total_testcases"] = len(testcases)

        # Minimum test case count
        if len(testcases) < MIN_TEST_CASES:
            errors.append(
                f"Minimum {MIN_TEST_CASES} test cases required. "
                f"Generated {len(testcases)}."
            )

        testcase_ids = set()
        descriptions = set()
        expected_results = set()
        complete_testcases = set()

        # Validate individual test cases
        for index, testcase in enumerate(testcases, start=1):

            if not isinstance(testcase, dict):
                errors.append(
                    f"Test Case {index} must be an object."
                )
                continue

            # Required fields
            for field in cls.REQUIRED_FIELDS:
                if field not in testcase:
                    errors.append(
                        f"Test Case {index}: "
                        f"Missing '{field}'."
                    )
                    statistics["missing_fields"] += 1

            testcase_id = cls._normalize(
                testcase.get("testCaseId", "")
            )

            description = cls._normalize(
                testcase.get("testDescription", "")
            )

            expected_result = cls._normalize(
                testcase.get("expectedResult", "")
            )

            steps = testcase.get("testSteps", [])

            # Test case ID uniqueness
            if REQUIRE_UNIQUE_TESTCASE_IDS and testcase_id:
                if testcase_id in testcase_ids:
                    errors.append(
                        f"Duplicate test case ID: "
                        f"'{testcase.get('testCaseId')}'."
                    )
                    statistics["duplicate_ids"] += 1
                else:
                    testcase_ids.add(testcase_id)

            # Test description uniqueness
            if REQUIRE_UNIQUE_DESCRIPTIONS and description:
                if description in descriptions:
                    warnings.append(
                        f"Test Case {index}: "
                        "Duplicate test description."
                    )
                    statistics["duplicate_descriptions"] += 1
                else:
                    descriptions.add(description)

            # Expected result duplicates
            if expected_result:
                if expected_result in expected_results:
                    warnings.append(
                        f"Test Case {index}: "
                        "Duplicate expected result."
                    )
                    statistics["duplicate_expected_results"] += 1
                else:
                    expected_results.add(expected_result)

            # Test steps
            if not isinstance(steps, list):
                errors.append(
                    f"Test Case {index}: "
                    "'testSteps' must be an array."
                )
                continue

            if len(steps) < MIN_TEST_STEPS:
                errors.append(
                    f"Test Case {index}: "
                    f"Minimum {MIN_TEST_STEPS} test steps required. "
                    f"Generated {len(steps)}."
                )
                statistics["invalid_step_count"] += 1

            # Duplicate steps within the same test case
            seen_steps = set()

            for step in steps:
                if not isinstance(step, str):
                    continue

                normalized_step = cls._normalize(step)

                if not normalized_step:
                    continue

                if normalized_step in seen_steps:
                    warnings.append(
                        f"Test Case {index}: "
                        f"Duplicate step detected: '{step}'."
                    )
                    statistics["duplicate_steps"] += 1
                else:
                    seen_steps.add(normalized_step)

            # Duplicate complete test case
            normalized_steps = tuple(
                cls._normalize(step)
                for step in steps
                if isinstance(step, str)
            )

            testcase_signature = (
                description,
                normalized_steps,
                expected_result,
            )

            if testcase_signature in complete_testcases:
                warnings.append(
                    f"Test Case {index}: "
                    "Duplicate complete test case."
                )
                statistics["duplicate_complete_testcases"] += 1
            else:
                complete_testcases.add(testcase_signature)

        score = 100 if not errors else 0

        return {
            "validator": "TestCaseValidator",
            "status": "SUCCESS" if not errors else "FAILED",
            "score": score,
            "errors": errors,
            "warnings": warnings,
            "statistics": statistics,
        }

    @staticmethod
    def _normalize(value) -> str:
        if value is None:
            return ""

        return " ".join(
            str(value)
            .strip()
            .lower()
            .split()
        )
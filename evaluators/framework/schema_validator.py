import json


class SchemaValidator:
    """
    Validates the generated LLM response
    against the expected QA Boat JSON schema.
    """

    REQUIRED_FIELDS = [
        "testCaseId",
        "testDescription",
        "testSteps",
        "expectedResult",
    ]

    @classmethod
    def validate(cls, generated_response) -> dict:

        errors = []

        # --------------------------------------------------
        # JSON Parsing
        # --------------------------------------------------

        if isinstance(generated_response, dict):

            parsed = generated_response

        else:

            try:

                parsed = json.loads(generated_response)

            except json.JSONDecodeError as exception:

                return {

                    "validator": "SchemaValidator",

                    "status": "FAILED",

                    "score": 0,

                    "valid_json": False,

                    "errors": [
                        f"Invalid JSON : {exception}"
                    ],

                    "data": None,

                }

        # --------------------------------------------------
        # Root Object
        # --------------------------------------------------

        if not isinstance(parsed, dict):

            errors.append(
                "Root element must be a JSON object."
            )

        # --------------------------------------------------
        # testCases
        # --------------------------------------------------

        testcases = parsed.get("testCases")

        if testcases is None:

            errors.append(
                "'testCases' key not found."
            )

        elif not isinstance(testcases, list):

            errors.append(
                "'testCases' must be an array."
            )

        else:

            for index, testcase in enumerate(testcases, start=1):

                if not isinstance(testcase, dict):

                    errors.append(
                        f"Test Case {index} is not an object."
                    )

                    continue

                for field in cls.REQUIRED_FIELDS:

                    if field not in testcase:
                        errors.append(
                            f"Test Case {index}: Missing '{field}'."
                        )

                if (
                    "testSteps" in testcase
                    and not isinstance(
                        testcase["testSteps"],
                        list,
                    )
                ):
                    errors.append(
                        f"Test Case {index}: 'testSteps' must be a list."
                    )

        # Result
        return {
            "validator": "SchemaValidator",

            "status": (
                "SUCCESS"
                if not errors
                else "FAILED"
            ),

            "score": (
                100
                if not errors
                else 0
            ),

            "valid_json": True,
            "errors": errors,
            "data": parsed,
        }
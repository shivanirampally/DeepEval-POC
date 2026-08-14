import json

class SchemaValidator:
    """
    Validates the generated QA Boat response
    against the expected QA Boat JSON structure.

    This validator checks structure only.
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

        # JSON Parsing
        if isinstance(generated_response, dict):
            parsed = generated_response

        else:

            try:
                parsed = json.loads(generated_response)

            except (json.JSONDecodeError,TypeError,) as exception:

                return {
                    "validator": "SchemaValidator",
                    "status": "FAILED",
                    "score": 0,
                    "valid_json": False,
                    "errors": [f"Invalid JSON : {exception}"],
                    "data": None,
                }

        # Root Object
        if not isinstance(parsed, dict):

            return {
                "validator": "SchemaValidator",
                "status": "FAILED",
                "score": 0,
                "valid_json": True,
                "errors": ["Root element must be a JSON object."],
                "data": None,
            }

        # testCases
        if "testCases" not in parsed:
            errors.append("'testCases' key not found.")

        else:
            testcases = parsed["testCases"]

            if not isinstance(testcases, list):
                errors.append("'testCases' must be an array.")

            else:
                for index, testcase in enumerate(testcases,start=1,):
                    # Test Case Object
                    if not isinstance(testcase,dict,):
                        errors.append(
                            f"Test Case {index} "
                            f"must be an object."
                        )
                        continue

                    # Required Fields
                    for field in cls.REQUIRED_FIELDS:

                        if field not in testcase:
                            errors.append(
                                f"Test Case {index}: "
                                f"Missing '{field}'."
                            )

                    # testSteps Type
                    if (
                        "testSteps" in testcase and not isinstance(testcase["testSteps"],list,)):
                        errors.append(
                            f"Test Case {index}: "
                            f"'testSteps' must be an array."
                        )

                    # Field Types
                    for field in ["testCaseId","testDescription","expectedResult",]:

                        if (
                            field in testcase
                            and not isinstance(testcase[field],str,)
                        ):

                            errors.append(
                                f"Test Case {index}: "
                                f"'{field}' must be a string."
                            )

        # Result
        return { "validator": "SchemaValidator",

            "status": ("SUCCESS" if not errors else "FAILED"),
            "score": (100 if not errors else 0),
            "valid_json": True,
            "errors": errors,
            "data": parsed
        }
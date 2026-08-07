import re


class CoverageValidator:
    """
    Validates whether generated test cases cover
    the business requirement.
    """

    POSITIVE_KEYWORDS = [
        "valid",
        "successful",
        "success",
        "correct",
        "allowed",
        "login",
        "submit",
        "save",
    ]

    NEGATIVE_KEYWORDS = [
        "invalid",
        "incorrect",
        "error",
        "failed",
        "fail",
        "empty",
        "mandatory",
        "required",
    ]

    BOUNDARY_KEYWORDS = [
        "minimum",
        "maximum",
        "boundary",
        "limit",
        "length",
        "min",
        "max",
    ]

    EDGE_KEYWORDS = [
        "special character",
        "null",
        "blank",
        "whitespace",
        "duplicate",
        "unexpected",
    ]

    VALIDATION_KEYWORDS = [
        "validation",
        "validate",
        "mandatory",
        "required",
        "format",
    ]

    @classmethod
    def validate(cls, requirement, generated_json):

        errors = []
        warnings = []
        score = 100

        statistics = {
            "requirement_lines": 0,
            "covered_requirement_lines": 0,
            "positive_scenarios": 0,
            "negative_scenarios": 0,
            "boundary_scenarios": 0,
            "edge_scenarios": 0,
            "validation_scenarios": 0,
            "business_rule_coverage": False,
        }

        testcases = generated_json.get(
            "testCases",
            [],
        )

        generated_text = ""
        for testcase in testcases:
            generated_text += " "
            generated_text += testcase.get(
                "testDescription",
                "",
            )

            generated_text += " "
            generated_text += testcase.get(
                "expectedResult",
                "",
            )

            generated_text += " "
            generated_text += " ".join(
                testcase.get(
                    "testSteps",
                    [],
                )
            )

        generated_text = generated_text.lower()

        # Requirement Coverage

        requirement_lines = [
            line.strip()
            for line in requirement.description.splitlines()
            if line.strip()
        ]

        statistics["requirement_lines"] = len(
            requirement_lines
        )

        covered = 0
        for line in requirement_lines:
            words = re.findall(
                r"\w+",
                line.lower(),
            )

            if not words:
                continue

            matches = sum(
                1
                for word in words
                if word in generated_text
            )

            if matches / len(words) >= 0.50:
                covered += 1

        statistics["covered_requirement_lines"] = covered

        if requirement_lines:
            coverage = (
                covered
                / len(requirement_lines)
            ) * 100

            if coverage < 100:
                warnings.append(
                    f"Requirement Coverage : {coverage:.0f}%"
                )
                score -= 10

        # Scenario Coverage

        def count_keywords(keywords):
            return sum(
                generated_text.count(word)
                for word in keywords
            )

        statistics["positive_scenarios"] = count_keywords(cls.POSITIVE_KEYWORDS)
        statistics["negative_scenarios"] = count_keywords(cls.NEGATIVE_KEYWORDS)
        statistics["boundary_scenarios"] = count_keywords(cls.BOUNDARY_KEYWORDS)
        statistics["edge_scenarios"] = count_keywords(cls.EDGE_KEYWORDS)
        statistics["validation_scenarios"] = count_keywords(cls.VALIDATION_KEYWORDS)

        if statistics["positive_scenarios"] == 0:
            warnings.append("Positive scenarios not detected.")
            score -= 5

        if statistics["negative_scenarios"] == 0:
            warnings.append("Negative scenarios not detected.")
            score -= 5

        if statistics["boundary_scenarios"] == 0:
            warnings.append("Boundary scenarios not detected.")
            score -= 5

        if statistics["edge_scenarios"] == 0:
            warnings.append("Edge scenarios not detected.")
            score -= 5

        if statistics["validation_scenarios"] == 0:
            warnings.append("Validation scenarios not detected.")
            score -= 5

        # Business Rules
        business_rules = (
            requirement.business_rules or ""
        ).strip()

        if business_rules:

            if business_rules.lower() in generated_text:

                statistics[
                    "business_rule_coverage"
                ] = True

            else:

                warnings.append(
                    "Business Rules not covered."
                )

                score -= 10

        return {

            "validator": "CoverageValidator",

            "status": "SUCCESS",

            "score": max(score, 0),

            "errors": errors,

            "warnings": warnings,

            "statistics": statistics,
        }
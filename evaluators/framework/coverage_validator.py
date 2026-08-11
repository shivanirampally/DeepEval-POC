import re

class CoverageValidator:
    """
    Evaluates requirement coverage using the Requirement as the
    primary source of truth and the Benchmark Repository as a
    reference repository.

    This validator does NOT directly compare against benchmark
    test cases. The benchmark is used only to identify potential
    missing or additional scenarios.
    """

    POSITIVE_KEYWORDS = [
        "valid",
        "success",
        "successful",
        "login",
        "submit",
        "save",
    ]

    NEGATIVE_KEYWORDS = [
        "invalid",
        "incorrect",
        "error",
        "failed",
        "mandatory",
        "required",
        "empty",
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
        "blank",
        "null",
        "duplicate",
        "whitespace",
        "special",
    ]

    @classmethod
    def validate(cls,requirement,generated_output,
    ):

        generated_cases = generated_output.get("testCases",[],)
        generated_text = ""

        for testcase in generated_cases:
            generated_text += " "
            generated_text += testcase.get("testDescription","")
            generated_text += " "
            generated_text += testcase.get("expectedResult", "")
            generated_text += " "
            generated_text += " ".join(
                testcase.get("testSteps",[])
            )

        generated_text = generated_text.lower()
        covered = []
        missing = []
        additional = []
        warnings = []
        errors = []
        score = 100

        # Requirement Coverage
        requirement_lines = [
            line.strip()

            for line in requirement.description.splitlines()
            if line.strip()
        ]

        for line in requirement_lines:

            words = re.findall(r"\w+",line.lower(),)
            if not words:continue

            matches = sum(
                1
                for word in words
                if word in generated_text
            )

            if matches / len(words) >= 0.50:covered.append(line)
            else:
                missing.append(line)

        if missing:
            score -= len(missing) * 5
            warnings.append(f"{len(missing)} requirement scenario(s) not covered.")

        # Benchmark Repository Analysis
        benchmark_descriptions = {
            testcase.description.lower()
            for testcase in requirement.benchmark_repository
        }

        generated_descriptions = {
            testcase.get("testDescription","").lower()
            for testcase in generated_cases
        }

        for scenario in generated_descriptions:
            if scenario not in benchmark_descriptions:
                additional.append(scenario)

        # Business Rule Coverage

        business_rules = (
            requirement.business_rules or ""
        ).strip()

        business_rule_covered = True

        if business_rules:

            keywords = re.findall(
                r"\w+",
                business_rules.lower(),
            )

            matched = sum(

                1

                for keyword in keywords

                if keyword in generated_text

            )

            if keywords:

                coverage = matched / len(keywords)

                if coverage < 0.50:

                    business_rule_covered = False

                    score -= 10

                    warnings.append(
                        "Business rules are partially covered."
                    )

        # Scenario Detection

        statistics = {

            "positive": cls._count_keywords(
                generated_text,
                cls.POSITIVE_KEYWORDS,
            ),

            "negative": cls._count_keywords(
                generated_text,
                cls.NEGATIVE_KEYWORDS,
            ),

            "boundary": cls._count_keywords(
                generated_text,
                cls.BOUNDARY_KEYWORDS,
            ),

            "edge": cls._count_keywords(
                generated_text,
                cls.EDGE_KEYWORDS,
            ),

        }

        # Requirement Satisfaction

        requirement_satisfied = (
            len(missing) == 0
            and business_rule_covered
        )

        if not requirement_satisfied:

            score -= 10

        score = max(score, 0)

        return {

            "validator": "Coverage Validator",

            "status": "SUCCESS",

            "score": score,

            "covered": covered,

            "missing": missing,

            "additional": additional,

            "requirement_satisfied": requirement_satisfied,

            "business_rule_covered": business_rule_covered,

            "statistics": statistics,

            "errors": errors,

            "warnings": warnings,

        }

    @staticmethod
    def _count_keywords(
        text,
        keywords,
    ):

        return sum(

            text.count(keyword)

            for keyword in keywords

        )
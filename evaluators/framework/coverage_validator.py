import re

from config.settings import (
    COVERAGE_MATCH_THRESHOLD,
    MIN_COVERAGE_PERCENTAGE,
)


class CoverageValidator:
    """
    Validates generated test case coverage against
    the requirement and approved benchmark repository.

    Empty benchmark sections are excluded from
    the coverage score.
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
    def validate(
        cls,
        requirement,
        generated_output,
    ) -> dict:

        errors = []
        warnings = []

        generated_cases = generated_output.get(
            "testCases",
            [],
        )

        generated_text = cls._build_generated_text(
            generated_cases
        )

        covered = []
        missing = []

        # Requirement coverage
        requirement_lines = [
            line.strip()
            for line in requirement.description.splitlines()
            if line.strip()
        ]

        for line in requirement_lines:

            if cls._text_matches(
                line,
                generated_text,
            ):
                covered.append(line)
            else:
                missing.append(line)

        # Business rule coverage
        business_rules = (
            requirement.business_rules or ""
        ).strip()

        business_rule_covered = True

        if business_rules:

            business_rule_covered = (
                cls._text_matches(
                    business_rules,
                    generated_text,
                )
            )

            if not business_rule_covered:

                warnings.append(
                    "Business rules are partially covered."
                )

        # Acceptance Criteria coverage
        acceptance_criteria = getattr(
            requirement,
            "acceptance_criteria",
            [],
        )

        acceptance_criteria_covered = 0
        acceptance_criteria_missing = 0

        for acceptance_criterion in acceptance_criteria:

            description = cls._normalize(
                getattr(
                    acceptance_criterion,
                    "description",
                    "",
                )
            )

            title = cls._normalize(
                getattr(
                    acceptance_criterion,
                    "title",
                    "",
                )
            )

            reference = (
                f"{description} {title}".strip()
            )

            if not reference:
                continue

            if cls._text_matches(
                reference,
                generated_text,
            ):
                acceptance_criteria_covered += 1
            else:
                acceptance_criteria_missing += 1

        if acceptance_criteria_missing:

            warnings.append(
                f"{acceptance_criteria_missing} "
                "acceptance criteria not covered."
            )

        # User Story benchmark coverage
        user_story_benchmarks = getattr(
            requirement,
            "user_story_benchmarks",
            [],
        )

        user_story_covered = 0
        user_story_missing = 0

        for benchmark in user_story_benchmarks:

            scenario = cls._normalize(
                getattr(
                    benchmark,
                    "scenario",
                    "",
                )
            )

            if not scenario:
                continue

            if cls._text_matches(
                scenario,
                generated_text,
            ):
                user_story_covered += 1
            else:
                user_story_missing += 1

        if user_story_missing:

            warnings.append(
                f"{user_story_missing} "
                "user story benchmark scenario(s) "
                "not covered."
            )

        # Coverage values
        coverage_values = []
        excluded_sections = []

        requirement_coverage = 100

        if requirement_lines:

            requirement_coverage = round(
                (
                    len(covered)
                    / len(requirement_lines)
                ) * 100,
                2,
            )

            coverage_values.append(
                requirement_coverage
            )
        else:
            excluded_sections.append(
                "Requirement coverage"
            )

        user_story_total = (
            user_story_covered
            + user_story_missing
        )

        user_story_coverage = 100

        if user_story_total:

            user_story_coverage = round(
                (
                    user_story_covered
                    / user_story_total
                ) * 100,
                2,
            )

            coverage_values.append(
                user_story_coverage
            )
        else:
            excluded_sections.append(
                "User Story benchmark coverage"
            )

        acceptance_total = (
            acceptance_criteria_covered
            + acceptance_criteria_missing
        )

        acceptance_coverage = 100

        if acceptance_total:

            acceptance_coverage = round(
                (
                    acceptance_criteria_covered
                    / acceptance_total
                ) * 100,
                2,
            )

            coverage_values.append(
                acceptance_coverage
            )
        else:
            excluded_sections.append(
                "Acceptance Criteria coverage"
            )

        # Overall coverage
        if coverage_values:

            overall_coverage = round(
                sum(coverage_values)
                / len(coverage_values),
                2,
            )

        else:

            overall_coverage = 0

        score = overall_coverage

        # Coverage quality gate
        if score < MIN_COVERAGE_PERCENTAGE:

            warnings.append(
                f"Coverage score is below the "
                f"{MIN_COVERAGE_PERCENTAGE}% threshold."
            )

        if missing:

            warnings.append(
                f"{len(missing)} requirement "
                "scenario(s) not covered."
            )

        # Excluded sections
        if excluded_sections:

            warnings.append(
                "Excluded from coverage score: "
                + ", ".join(excluded_sections)
                + " because no data was provided."
            )

        statistics = {

            "requirement_coverage":
                requirement_coverage,

            "user_story_coverage":
                user_story_coverage,

            "acceptance_criteria_coverage":
                acceptance_coverage,

            "requirement_total":
                len(requirement_lines),

            "requirement_covered":
                len(covered),

            "requirement_missing":
                len(missing),

            "user_story_total":
                user_story_total,

            "user_story_covered":
                user_story_covered,

            "user_story_missing":
                user_story_missing,

            "acceptance_criteria_total":
                acceptance_total,

            "acceptance_criteria_covered":
                acceptance_criteria_covered,

            "acceptance_criteria_missing":
                acceptance_criteria_missing,

            "excluded_sections":
                excluded_sections,

            "positive":
                cls._count_keywords(
                    generated_text,
                    cls.POSITIVE_KEYWORDS,
                ),

            "negative":
                cls._count_keywords(
                    generated_text,
                    cls.NEGATIVE_KEYWORDS,
                ),

            "boundary":
                cls._count_keywords(
                    generated_text,
                    cls.BOUNDARY_KEYWORDS,
                ),

            "edge":
                cls._count_keywords(
                    generated_text,
                    cls.EDGE_KEYWORDS,
                ),
        }

        return {

            "validator": "CoverageValidator",

            "status": "SUCCESS",

            "score": score,

            "covered": covered,

            "missing": missing,

            "requirement_satisfied": (
                not missing
                and business_rule_covered
            ),

            "business_rule_covered":
                business_rule_covered,

            "statistics": statistics,

            "errors": errors,

            "warnings": warnings,
        }

    @staticmethod
    def _build_generated_text(
        generated_cases,
    ) -> str:

        parts = []

        for testcase in generated_cases:

            parts.append(
                testcase.get(
                    "testDescription",
                    "",
                )
            )

            parts.append(
                testcase.get(
                    "expectedResult",
                    "",
                )
            )

            parts.extend(
                testcase.get(
                    "testSteps",
                    [],
                )
            )

        return " ".join(
            str(value)
            for value in parts
            if value
        ).lower()

    @staticmethod
    def _text_matches(
        reference,
        generated_text,
    ) -> bool:

        words = re.findall(
            r"\w+",
            reference.lower(),
        )

        if not words:
            return True

        matches = sum(
            1
            for word in words
            if word in generated_text
        )

        return (
            matches / len(words)
            >= COVERAGE_MATCH_THRESHOLD
        )

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

    @staticmethod
    def _count_keywords(
        text,
        keywords,
    ) -> int:

        return sum(
            text.count(keyword)
            for keyword in keywords
        )
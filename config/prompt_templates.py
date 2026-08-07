"""
DeepEval Evaluation Criteria
These prompts are used by GEval metrics to semantically evaluate
generated test cases against business requirements.
"""

# Correctness
CORRECTNESS_CRITERIA = """
Evaluate whether the generated test cases correctly satisfy the
expected output (reference test cases).

Evaluate:
1. Functional correctness
2. Expected behaviour
3. Validations
4. Missing scenarios
5. Incorrect scenarios

Ignore wording and formatting differences.

Return a high score only when the generated test cases are
functionally equivalent to the expected output.
"""

# Hallucination
HALLUCINATION_CRITERIA = """
Evaluate whether the generated test cases contain scenarios that
are unsupported by the requirement or business rules.

Penalize:
1. Invented functionality
2. Unsupported validations
3. Imaginary workflows
4. Assumptions not present in the requirement

Return a high score only when every generated test case is
grounded in the requirement.
"""

# Faithfulness
FAITHFULNESS_CRITERIA = """
Evaluate whether every generated test case is directly supported
by the provided requirement and business rules.

Evaluate:
1. Requirement grounding
2. Business rule alignment
3. Functional consistency

Penalize:
- Hallucinated scenarios
- Unsupported assumptions
- Invented validations

Return a high score only when every generated test case is
faithfully derived from the requirement.
"""

# Completeness
COMPLETENESS_CRITERIA = """
Evaluate whether the generated test cases completely cover the
business requirement and its acceptance criteria.

Evaluate:
1. Positive scenarios
2. Negative scenarios
3. Boundary value scenarios
4. Input validation scenarios
5. Exception handling
6. Expected results
7. Test data coverage

Ignore writing style.

Return a high score only when the generated test cases provide
complete functional coverage with minimal missing scenarios.
"""

# Context Precision
CONTEXT_PRECISION_CRITERIA = """
Evaluate whether only relevant information from the requirement
has been used while generating the test cases.

Evaluate:
1. Requirement relevance
2. Business rule relevance
3. Scenario relevance

Penalize:
- Unnecessary scenarios
- Irrelevant functionality
- Redundant validations

Return a high score when every generated test case is directly
related to the requirement.
"""

# Context Recall
CONTEXT_RECALL_CRITERIA = """
Evaluate whether all important information present in the
requirement has been reflected in the generated test cases.

Evaluate:
1. Acceptance criteria coverage
2. Business rule coverage
3. Functional flow coverage
4. Validation coverage

Penalize:
- Missing scenarios
- Ignored validations
- Missing business rules

Return a high score when no important information has been omitted.
"""

# Business Rule Coverage
BUSINESS_RULE_CRITERIA = """
Evaluate whether every business rule defined in the requirement
has been validated by one or more generated test cases.

Evaluate:
1. Every business rule is covered.
2. Expected behaviour matches the rule.
3. Invalid rule handling is validated.
4. No business rule is missing.

Ignore formatting differences.

Return a high score only when all business rules are validated.
"""

# Requirement Satisfaction
REQUIREMENT_CRITERIA = """
Evaluate whether the generated test cases fully satisfy the
original business requirement.

Evaluate:
1. Functional coverage
2. Acceptance criteria coverage
3. User workflow
4. Expected business outcome

Ignore wording differences.

Return a high score only when the generated test cases satisfy
the complete intent of the requirement.
"""

# Answer Relevancy
ANSWER_RELEVANCY_CRITERIA = """
Evaluate whether the generated test cases are relevant to the
given business requirement.

Evaluate:
1. Relevance to the requirement
2. Appropriate test scenarios
3. Correct functional scope
4. Meaningful validations

Penalize:
- Irrelevant scenarios
- Unrelated functionality
- Duplicate or unnecessary test cases

Return a high score only when every generated test case is
directly relevant to the requirement.
"""
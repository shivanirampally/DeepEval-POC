def build_story_expansion_prompt(
    title: str,
    description: str,
    acceptance_section: str,
    knowledge_section: str,
) -> str:
    print("story expansion prompt from ollama")
    return f"""
You are a senior QA analyst. Expand the user story into a strict JSON object.

RESPONSE RULES:
- Return JSON only. No markdown, no code fences, no commentary.
- The response MUST start with {{ and end with }}.
- Do NOT include any text before or after the JSON object.
- Do NOT wrap the JSON in ```json fences.
- Keep wording deterministic and stable for the same input. Do not restate the same idea with synonyms.
- Keep list ordering stable: follow the acceptance-criteria order first, then supporting details.
- Preserve every acceptance criterion, including exact limits, formats, statuses, timings, integrations, and rejection rules.
- functional_insights must contain one distinct item for every acceptance criterion, in the same order.
- Do not combine criteria when doing so would hide a constraint.
- edge_risks may only describe a boundary, validation rule, restriction, or failure condition explicitly stated in the story or acceptance criteria.
- Do not invent business behaviour, error messages, user roles, failure handling, or risks.

JSON SCHEMA:
{{
  "summary": "<1-2 sentences>",
  "narrative": ["<bullet 1>", "<bullet 2>"],
  "functional_insights": ["<insight 1>", "<insight 2>"],
  "edge_risks": ["<risk 1>", "<risk 2>"]
}}

### Original User Story
Title: {title}
Description: {description}

### Acceptance Criteria
{acceptance_section}
{knowledge_section}
""".strip()


def build_story_validation_prompt(
    title: str,
    description: str,
    acceptance_section: str,
    candidate_payload_json: str,
) -> str:
    return f"""
You are a meticulous QA validation assistant. Validate and correct the JSON expansion.

RULES:
- Return JSON only. No markdown, no code fences, no commentary.
- The response MUST start with {{ and end with }}.
- Do not remove fields; correct or refine them.
- Do NOT include any text before or after the JSON object.
- Do NOT wrap the JSON in ```json fences.
- Preserve every acceptance criterion and every exact constraint from it.
- functional_insights must contain one distinct item per acceptance criterion in the original order.
- Remove unsupported assumptions; edge_risks must be directly grounded in the supplied requirements.

JSON SCHEMA:
{{
  "summary": "<1-2 sentences>",
  "narrative": ["..."],
  "functional_insights": ["..."],
  "edge_risks": ["..."]
}}

### Original Story
Title: {title}
Description: {description}
Acceptance Criteria:
{acceptance_section}

### Candidate JSON
{candidate_payload_json}
""".strip()


def build_task_breakdown_prompt(
    title: str,
    story_json: str,
    acceptance_criteria_json: str,
    min_tasks: int,
    max_tasks: int,
) -> str:
    return f"""
You are a senior delivery lead producing implementable tasks for QA enablement.

RESPONSE RULES:
- Return JSON only. No markdown, no code fences, no commentary.
- The response MUST start with {{ and end with }}.
- Do NOT include any text before or after the JSON object.
- Do NOT wrap the JSON in ```json fences.
- Produce between {min_tasks} and {max_tasks} distinct tasks. Prefer the smallest complete set.
- Acceptance criteria are arbitrary free-text items; AC1..ACn are internal IDs assigned only by list position.
- Keep taskId sequential (T1, T2, ...). No duplicates.
- Combine closely related acceptance criteria when they describe the same implementation behavior.
- Do not create separate implementation and validation tasks for the same behavior.
- Every acceptance criterion must remain covered by at least one task.
- acceptanceTrace MUST be an array of AC IDs only (AC1, AC2, ...). Do NOT include any free-text in acceptanceTrace.
- Use a stable order: core implementation first, validation next, integrations after that, then audit/support tasks.
- Do not create two tasks that test or deliver the same intent with different wording.
- Never produce generic task names such as "Acceptance coverage task", "QA support task", or "Implement and verify AC#".
JSON SCHEMA:
{{
    "tasks": [
        {{
            "taskId": "T1",
            "name": "<short task name>",
            "intent": "<what this task delivers>",
            "acceptanceTrace": ["AC1", "AC2"],
            "doneWhen": "<observable completion signal>",
            "dependencies": ["<systems/APIs/data>"]
        }}
    ]
}}

TITLE: {title}
EXPANDED STORY JSON:
{story_json}

ACCEPTANCE CRITERIA:
{acceptance_criteria_json}
""".strip()


def build_task_breakdown_repair_prompt(
    title: str,
    story_json: str,
    acceptance_criteria_json: str,
    candidate_tasks_json: str,
    issues_json: str,
) -> str:
    return f"""
You are a senior delivery lead repairing a task breakdown.

Return strict JSON only using the same task schema as the candidate.

REPAIR RULES:
- Acceptance criteria are arbitrary free-text items identified internally as AC1..ACn by their list position.
- Every supplied AC ID must appear in at least one acceptanceTrace.
- Use the smallest cohesive set of implementation tasks; there is no minimum task count.
- Merge closely related criteria when they represent one implementation behavior or complementary states.
- Every task name must describe a real implementation outcome.
- Never use generic names such as "Acceptance coverage task", "QA support task", or "Implement and verify AC#".
- Keep name, intent, doneWhen, dependencies, and acceptanceTrace aligned to one responsibility.
- Do not invent behavior outside the story and acceptance criteria.
- Remove duplicate or overlapping tasks and return sequential task IDs.

TITLE: {title}
EXPANDED STORY JSON: {story_json}
ACCEPTANCE CRITERIA: {acceptance_criteria_json}
CANDIDATE TASKS: {candidate_tasks_json}
DETECTED ISSUES: {issues_json}
""".strip()


def build_requirements_inventory_prompt(story_compact: str, ac_block: str) -> str:
    return f"""
You are a QA requirements engineer. From the user story, infer additional *testable* requirements beyond acceptance criteria.

Return STRICT JSON only (no markdown, no backticks).

Focus on what real QA covers:
- validations & input constraints
- roles & permissions
- state transitions
- error handling & resiliency
- integrations / dependencies
- audit/logging/notifications when relevant
- non-functional (performance, accessibility, security) ONLY if suggested by the story

Do NOT invent completely unrelated scope. If something is unknown, phrase it as an assumption-based requirement and tag it with "assumption".

JSON schema:
{{
  "acceptanceCriteriaAnalysis": [
    {{
      "id": "AC1",
      "behavior": "<single behavior being required>",
      "conditions": ["<explicit condition or input>"],
      "expectedOutcome": "<explicit observable outcome>",
      "explicitConstraints": ["<only limits/rules explicitly stated in the AC or story>"]
    }}
  ],
  "derivedRequirements": [
    {{
      "statement": "<one requirement sentence>",
      "category": "Validation" | "Permissions" | "State" | "ErrorHandling" | "Integration" | "NonFunctional" | "Functional",
      "priority": "High" | "Medium" | "Low",
      "tags": ["assumption", "security", "performance", "accessibility", "data"]
    }}
  ]
}}

USER STORY (MARKDOWN):
{story_compact}

ACCEPTANCE CRITERIA INDEX:
{ac_block}
""".strip()


def build_coverage_prompt(criteria_block: str, deterministic_trace_json: str) -> str:
    return f"""
Act as a QA coverage analyst. Compare the provided USER STORY and the generated TEST CASES, then output a JSON payload ONLY.

OBJECTIVE:
- Summarize coverage strength.
- Highlight distribution across scenario types.
- Explicitly call out gaps per acceptance criterion.
- Suggest remedial tests.

INPUTS ARE MARKDOWN. DO NOT ECHO THEM BACK.

RESPONSE FORMAT (STRICT JSON, NO MARKDOWN, NO BACKTICKS):
{{
  "summary": {{
    "coverageScore": <integer 0-100>,
    "riskLevel": "Low" | "Medium" | "High",
    "confidence": "High" | "Medium" | "Low",
    "highlights": ["...", "..."]
  }},
  "scenarioMix": {{
    "labels": ["Positive", "Negative", "Edge", "Integration"],
    "values": [<int>, <int>, <int>, <int>]
  }},
  "criteriaCoverage": [
    {{
      "criterion": "<acceptance criterion paraphrased>",
      "status": "covered" | "partial" | "missing",
      "linkedTests": ["TC1.1", "TC3.2"],
      "note": "<short justification>"
    }}
  ],
  "gapInsights": [
    {{
      "title": "<gap headline>",
      "detail": "<what is untested>",
      "recommendedTest": "<idea for new test>"
    }}
  ]
}}

STRICT RULES:
- Return JSON only. No prose, no code fences.
- Do NOT include any text before or after the JSON object.
- Do NOT wrap the JSON in ```json fences.
- Populate every section. Use an empty array [] when no items.
- scenarioMix.labels MUST remain exactly as provided.

### ACCEPTANCE CRITERIA INDEX
{criteria_block}

### DETERMINISTIC TRACEABILITY SUMMARY (JSON)
{deterministic_trace_json}
""".strip()


def build_markdown_to_html_prompt(markdown_content: str, section_class: str) -> str:
  return f"""
You are a presentation-focused formatter. Convert the markdown input into semantic HTML that renders well in QA dashboards.

### Markdown Input
{markdown_content}

OUTPUT RULES:
1. Return ONLY an HTML fragment (no markdown fences, no commentary).
2. Wrap all content inside `<section class=\"{section_class}\">` ... `</section>`.
3. Promote markdown headings to matching HTML heading levels (use h2+), keep ordered and unordered lists intact, and convert paragraphs into `<p>`.
4. You may group related content in `<article>` blocks, include `<hr />` between logical sections, and use `<strong>`/`<em>` for emphasis.
5. Never change or omit the underlying text—only render the formatting.
6. Allowed tags: section, article, header, h2-h4, p, ul, ol, li, hr, strong, em, span, code, pre, blockquote, table, thead, tbody, tr, th, td, br.
"""


def build_html_to_markdown_prompt(html_content: str) -> str:
  return f"""
You are a documentation assistant. Convert the provided HTML fragment into clean markdown.

### HTML Input
{html_content}

RULES:
1. Preserve every heading, paragraph, bullet, number list, table, and emphasized span.
2. Output ONLY markdown (no explanations, no HTML, no code fences).
3. Start directly with the first heading or paragraph from the source.
4. Maintain the same wording—do not summarize or elaborate.
"""


def build_generate_testcases_prompt(ado_task_details_json: str, knowledge_doc_section: str) -> str:
    return f"""You are an expert QA engineer. Your response MUST be ONLY valid JSON with NO additional text.

CRITICAL INSTRUCTIONS:
- Your response MUST start with {{ and end with }}
- NO introductory text like "Here is the JSON output:"
- NO markdown code blocks (no ```json or ```)
- NO explanations before or after the JSON
- NO comments inside the JSON
- Output ONLY the raw JSON object
- You MUST analyze the task details and generate REAL test cases, NOT placeholder examples

--- ADO TASK DETAILS ---
{ado_task_details_json}

{knowledge_doc_section}

--- YOUR TASK ---
Analyze the ADO task details above and generate realistic, thorough test cases that validate the specific functionality described.

--- REQUIRED JSON SCHEMA ---

Return a JSON object matching this EXACT structure.
IMPORTANT: Replace ALL placeholder values with ACTUAL test cases based on the ADO task above.
DO NOT return these placeholder values - generate real test cases specific to the task.

{{
  "testCases": [
    {{
      "testCaseId": "<GENERATE_UNIQUE_ID_LIKE_TC001>",
      "testDescription": "<WRITE_SPECIFIC_TEST_DESCRIPTION_FOR_THIS_TASK>",
      "testSteps": [
        "<STEP_1_SPECIFIC_ACTION>",
        "<STEP_2_SPECIFIC_ACTION>"
      ],
      "expectedResult": "<EXPECTED_OUTCOME_FOR_THIS_SPECIFIC_TEST>"
    }}
  ]
}}

FIELD DESCRIPTIONS:

1. testCaseId (string):
   - Format: "TC" followed by sequential numbers (TC001, TC002, TC003, etc.)
   - Must be unique for each test case
   - Start from TC001 and increment

2. testDescription (string):
   - Clear, specific description of what this test validates
   - Must be directly related to the ADO task requirements
   - Examples: "Validate login with correct credentials", "Verify error message for invalid email format"

3. testSteps (array of strings):
   - Each step is a specific action the tester must perform
   - Write clear, actionable steps (e.g., "Enter valid email and password", "Click the Submit button")
   - Include at least 2-5 steps per test case
   - Steps should be sequential and logical

4. expectedResult (string):
   - Single sentence describing the expected outcome after completing all steps
   - Must be specific and measurable
   - Examples: "User is redirected to dashboard", "Error message 'Invalid email format' is displayed"

TEST CASE GENERATION REQUIREMENTS:

1. ANALYZE THE ADO TASK: Read the Description and Acceptance Criteria carefully
2. GENERATE MULTIPLE TEST CASES: Create at least 5-10 test cases covering:
   - Positive scenarios (happy path)
   - Negative scenarios (error cases, invalid inputs)
   - Edge cases (boundary conditions, empty fields, special characters)
   - Integration scenarios (if applicable)

3. MAP TO ACCEPTANCE CRITERIA: Each acceptance criterion should have at least one corresponding test case

4. BE SPECIFIC: Test cases must be directly relevant to the ADO task, not generic examples

5. USE REALISTIC DATA: Reference actual fields, buttons, and features mentioned in the task

VALIDATION RULES:
- All field names must use double quotes
- All string values must use double quotes
- testCases array must contain at least 5 test cases
- Each test case must have all 4 required fields
- testSteps array must have at least 2 steps
- No trailing commas
- All brackets must be properly closed

IMPORTANT REMINDERS:
- DO NOT copy the placeholder example above
- DO NOT use generic test descriptions like "Test case 1" or "Validate functionality"
- DO analyze the specific ADO task and create relevant test cases
- DO ensure test cases directly address the requirements in the task

YOUR RESPONSE MUST START WITH {{ AND END WITH }}

Analyze the ADO task above and generate specific test cases now:"""


def build_json_repair_prompt(raw_text: str) -> str:
  return f"""
  You are a JSON repair engine designed to fix malformed JSON produced by an LLM.

  Your job:
  Given the text below, locate the JSON object (even if broken), repair it, and return
  a single valid JSON object that can be parsed by Python json.loads() without errors.

  ### STRICT RULES (MUST FOLLOW)
  1. Output ONLY valid JSON. No text, no commentary, no markdown, no code fences.
  2. Preserve all keys, structure, meaning, and fields from the original content.
  3. Fix ALL JSON issues, including:
  - missing commas
  - missing quotes
  - extra commas
  - unescaped characters
  - mismatched or missing brackets/braces
  - mixed text + JSON
  - duplicated keys
  4. If text exists before or after JSON, ignore it completely.
  5. Do NOT invent new fields or remove required ones.
  6. The final output MUST be syntactically perfect JSON that json.loads() can parse.

  --- Text ---
  {raw_text}
  ---

  Return ONLY valid JSON that can be parsed by json.loads()
  """


def build_qa_insights_prompt(
    workitem_details_json: str,
    generated_testcases_json: str,
    knowledge_doc_section: str,
) -> str:
  return f"""You are a Senior QA Analyst AI. Your response MUST be ONLY valid JSON with no additional text, explanations, or markdown formatting.

CRITICAL INSTRUCTIONS:
- Output ONLY the JSON object starting with {{ and ending with }}
- NO markdown code blocks (no ```json or ```)
- NO explanatory text before or after the JSON
- NO comments inside the JSON
- All string values must use double quotes, not single quotes
- All numbers must be valid integers
- Ensure all brackets and braces are properly closed
- You MUST analyze the provided data and generate REAL values, NOT placeholder values

--- INPUT DATA ---

WORK ITEM DETAILS:
{workitem_details_json}

GENERATED TEST CASES:
{generated_testcases_json}

{knowledge_doc_section}

--- REQUIRED JSON OUTPUT SCHEMA ---

You MUST return a JSON object with this EXACT structure.
IMPORTANT: Replace ALL placeholder values with your ACTUAL ANALYSIS of the input data above.
DO NOT return these placeholder values - calculate and provide real values based on the work item and test cases.

{{
  "coverage_summary": {{
    "total_acceptance_criteria": <COUNT_TOTAL_AC_FROM_WORKITEM>,
    "covered_criteria": <COUNT_COVERED_AC_BY_TESTCASES>,
    "coverage_percentage": <CALCULATE_PERCENTAGE>,
    "missing_criteria": ["<DESCRIBE_EACH_MISSING_CRITERION>"]
  }},
  "testcase_quality": {{
    "positive_scenarios": <COUNT_POSITIVE_TESTS>,
    "negative_scenarios": <COUNT_NEGATIVE_TESTS>,
    "edge_cases": <COUNT_EDGE_CASE_TESTS>,
    "integration_scenarios": <COUNT_INTEGRATION_TESTS>,
    "other_scenarios": <COUNT_OTHER>
  }},
  "risk_assessment": {{
    "risk_level": "<Low_OR_Medium_OR_High>",
    "risk_factors": ["<LIST_ACTUAL_RISK_FACTORS>"]
  }},
  "missing_test_scenarios": ["<LIST_ACTUAL_MISSING_SCENARIOS>"],
  "overall_quality_score": <CALCULATE_SCORE_0_TO_100>,
  "graph_data": {{
    "coverage_pie": {{
      "labels": ["Covered", "Uncovered"],
      "values": [<COVERED_PERCENTAGE>, <UNCOVERED_PERCENTAGE>]
    }},
    "testcase_type_distribution": {{
      "labels": ["Positive", "Negative", "Edge", "Integration", "Other"],
      "values": [<POS>, <NEG>, <EDGE>, <INT>, <OTHER>]
    }},
    "radar_quality_metrics": {{
      "labels": ["Coverage", "AC Clarity", "Test Depth", "Risk"],
      "values": [<COVERAGE_SCORE>, <CLARITY_SCORE>, <DEPTH_SCORE>, <RISK_SCORE>]
    }}
  }}
}}

FIELD DESCRIPTIONS AND VALIDATION RULES:

1. coverage_summary - ANALYZE THE WORK ITEM:
   - total_acceptance_criteria: Count how many acceptance criteria exist in the work item (integer)
   - covered_criteria: Count how many are covered by the generated test cases (integer)
   - coverage_percentage: Calculate (covered_criteria / total_acceptance_criteria) * 100 (integer 0-100)
   - missing_criteria: List each specific criterion that lacks test coverage (array of strings)

2. testcase_quality - CATEGORIZE THE TEST CASES:
   - positive_scenarios: Count test cases testing happy/success paths (integer >= 0)
   - negative_scenarios: Count test cases testing errors/failures (integer >= 0)
   - edge_cases: Count test cases testing boundaries/limits (integer >= 0)
   - integration_scenarios: Count test cases testing system integration (integer >= 0)
   - other_scenarios: Count any test cases that do not fit above categories (integer >= 0)

   IMPORTANT COUNT CONSISTENCY RULES:
    - You MUST classify EVERY test case provided in GENERATED TEST CASES.
    - No test case can be skipped, merged, or left unclassified.
    - You are NOT allowed to create new categories or combine categories.
    - Each test case MUST belong to exactly one category (positive, negative, edge, integration, other).
    - The sum of all four values (positive_scenarios + negative_scenarios + edge_cases + integration_scenarios + other_scenarios)
    MUST equal the TOTAL number of test cases in GENERATED TEST CASES.
    - This is a HARD REQUIREMENT: If the total does NOT match, you MUST correct your classification
    BEFORE outputting the JSON.
    - The values used in graph_data.testcase_type_distribution.values MUST exactly match the values in
    testcase_quality in this order: [positive_scenarios, negative_scenarios, edge_cases, integration_scenarios, other_scenarios].
    - If a test case could fit multiple categories, you MUST select the closest single matching category—
    but you cannot leave it unclassified.
    - A fifth category "other_scenarios" MUST be used for any test case that does not fit clearly into
  positive, negative, edge, or integration.
    - The sum of all five values (positive_scenarios + negative_scenarios + edge_cases +
    integration_scenarios + other_scenarios) MUST equal the total number of generated test cases.
    - No test case may be left unclassified for any reason.
    - graph_data.testcase_type_distribution MUST use the same five categories and the same counts in
    this exact order: ["Positive", "Negative", "Edge", "Integration", "Other"].
  """


def build_task_suite_prompt(
    task_id: str,
    task_name: str,
    story_summary: str,
    acceptance_block: str,
    derived_block: str,
    other_tasks_block: str,
    task_context: str,
) -> str:
    return f"""
You are a principal QA architect. Generate exhaustive manual test cases for the task below.

STRICT RULES:
- Return JSON only. No markdown, no code fences, no commentary.
- The response MUST start with {{ and end with }}.
- Do NOT include any text before or after the JSON object.
- Do NOT wrap the JSON in ```json fences.
- Generate only distinct scenarios supported by the current task and its listed acceptance criteria.
- As non-binding mix guidance for a normal user story, aim near Positive 30-40%, Negative 25-35%, Edge 20-25%, Integration 15-20%. Do not manufacture, duplicate, omit, or relabel cases to reach these percentages; the acceptance criteria always override the mix.
- Do not invent Negative, Edge, or Integration behavior when it is not supported by the listed criteria.
- Every test case MUST reference only AC# values listed for this task; do not use R# refs.
- Generate test cases ONLY for the CURRENT TASK below.
- Do NOT include cases that belong to other tasks listed below.
- Each testcase must validate exactly one condition and one observable outcome.
- Do not combine two validation failures or two independent checks in one testcase. Example pattern to avoid: invalid value + invalid format in the same case.
- Each testcase must reference exactly one AC ID. Split multi-AC workflows into atomic outcome cases.
- The referenced AC must directly describe the behavior being tested; do not map a case to a nearby AC from the same task.
- `expected` must be one string, never an array or object.
- Preconditions are setup only; steps are executable actions only; system outcomes belong only in `expected`.
- Use only conditions, limits, messages, and state behavior supported by the listed AC text or structured assertions.
- Do not introduce a screen, tool, channel, access method, data source, user role, message text, or verification mechanism unless it appears in the current task or mapped AC text.
- If the AC says a record/email/API/update occurs, test that observable outcome directly; do not invent how QA accesses it unless the task/AC says the access method.
- A testcase is a duplicate if it validates the same behavior/outcome with only wording changes. Do not generate semantic duplicates.
- Treat two cases as duplicates when they validate the same condition and same outcome with only wording changes, even if the scenario label differs.
- Do not create an Edge case unless the AC has an explicit boundary or limit such as at least, at most, minimum, maximum, exactly, future date, or past date.
- Do not create an Integration case unless the AC explicitly describes an interaction with another system, channel, or persisted state transition.
- Do not invent exact error text, success text, redirect behavior, retry logic, role behavior, token behavior, or hidden prerequisites unless the AC explicitly states them.
- Make every step concrete and executable. Do not write generic template steps such as "perform the action stated in the acceptance criterion."
- Do not copy the acceptance criterion text verbatim into title, steps, or expected. Convert it into concrete user/system actions and one observable outcome.
- A single step like "Verify that <acceptance criterion>" is invalid. Use at least two concrete chronological steps whenever interaction is required.
- Classify cancellation, blocked login attempts, invalid sessions, denied access, or prevented actions as Negative when they are the behavior being validated.
- Classify cross-browser, cross-device, previous-session replacement, persisted session state, or multi-client behavior as Integration when those interactions are being validated.
- Classify explicit limits such as "only one", "at a time", "exactly", "maximum", or "minimum" as Edge when the testcase validates that boundary.
- Write steps in executable chronological order: establish/navigate to the required state, verify the control is visible, then interact with it, then observe the result. Never select, click, enter, or inspect an element before the steps make that element available.
- Use stable wording for the same input and keep testcase ordering fixed as: Positive, Negative, Edge, Integration, then any extras.
- Each testcase title must include task-specific nouns from the current task so it is distinguishable from neighboring tasks.

JSON SCHEMA:
{{
  "taskId": "{task_id}",
  "taskName": "{task_name}",
  "testCases": [
    {{
      "id": "TC{task_id}.1",
      "title": "<case title>",
      "scenarioType": "Positive | Negative | Edge | Integration",
      "preconditions": ["<precondition>", "..."],
      "steps": ["<step 1>", "<step 2>"],
      "expected": "<expected result>",
      "refs": ["AC1"]
    }}
  ]
}}

### STORY SUMMARY
{story_summary}

### ACCEPTANCE CRITERIA INDEX
{acceptance_block}

### DERIVED REQUIREMENTS INDEX (R#)
{derived_block}

### OTHER TASKS (DO NOT COVER)
{other_tasks_block}

### TASK CONTEXT
{task_context}
""".strip()


def build_task_audit_prompt(
    story_summary: str,
    acceptance_block: str,
    task_context: str,
    other_tasks_block: str,
    existing_cases_json: str,
) -> str:
    return f"""
You are a QA coverage auditor. Evaluate the task test cases and return a strict JSON gap report.

RULES:
- Audit only the acceptance criteria listed below for this task.
- Do not force scenario types that are not supported by those criteria.
- Do not propose cases belonging to another task.
- Validate testcase meaning, not merely whether its refs contain an allowed AC ID.
- A testcase is grounded only when its condition, action, and expected outcome are supported by the task and at least one referenced AC.
- If the testcase behavior is better supported by another AC than its referenced AC, repair the refs or remove the case.
- Put cases that test another task, unsupported assumptions, contradictions, or semantic duplicates in removeCaseIds.
- For duplicates, keep the clearest and most complete case and remove the others.
- Treat paraphrases as duplicates even when titles differ or the scenario label changes.
- Use replacementCases to correct a valuable case whose refs, steps, or expected result are misaligned.
- Replacement cases must retain the original ID and contain the complete testcase object.
- Steps must be executable actions; expected outcomes must be in expected, not written as steps.
- Preconditions must establish setup and must not assert that the behavior under test already happened.
- Do not remove a distinct case merely because it shares an AC with another scenario.
- For every existing case, include caseEvaluations with direct support evidence from the listed AC text or structured assertion.
- If a limit, state transition, retry, token behavior, role, message, or failure outcome has no evidence, list it in unsupportedClaims and remove the case.
- If a case introduces a screen, tool, channel, access method, data source, user role, message text, or verification mechanism not present in the task/AC text, list it in unsupportedClaims and repair or remove the case.
- A shared AC ID is not evidence by itself.
- When a Positive and Edge case express the same behavior, keep only the one that uses a true explicit boundary input.
- Remove any case whose steps are vague, generic, or not directly executable from the AC text.
- Remove any case that merely repeats the acceptance criterion in title, steps, or expected instead of describing executable setup/actions and an observable result.
- Repair cases that are mislabeled Positive when their behavior is cancellation, blocked access, invalidated session, cross-browser/device validation, or explicit boundary validation.
- Repair or remove any case whose actions are out of order, including interacting with a control before navigating to or displaying it.

JSON SCHEMA:
{{
  "caseEvaluations": [
    {{
      "caseId": "TCT1.1",
      "decision": "keep | repair | remove",
      "supportingAC": "AC1",
      "supportEvidence": "<short evidence from AC text/structured assertion>",
      "unsupportedClaims": [],
      "reason": "<concise semantic judgment>"
    }}
  ],
  "missingScenarioTypes": ["Positive", "Negative", "Edge", "Integration"],
  "missingAcceptanceRefs": ["AC1", "AC2"],
  "missingCases": [
    {{
      "scenarioType": "Positive",
      "title": "<what is missing>",
      "ref": "AC1"
    }}
  ],
  "removeCaseIds": ["TCT1.3"],
  "replacementCases": [
    {{
      "id": "TCT1.1",
      "title": "<corrected case title>",
      "scenarioType": "Positive | Negative | Edge | Integration",
      "preconditions": ["<setup only>"],
      "steps": ["<executable action>"],
      "expected": "<observable result supported by the AC>",
      "refs": ["AC1"]
    }}
  ]
}}

Analyze every AC ID. Do not invent constraints or user feedback. Use an empty array when no condition or constraint is explicit.
The expectedOutcome must contain only outcomes explicitly stated by the AC/story. If validation or prevention is required but no message is specified, state only that the action is rejected or prevented; never invent an error/success message, redirect, notification content, retry, or UI state.

### STORY SUMMARY
{story_summary}

### ACCEPTANCE CRITERIA INDEX
{acceptance_block}

### TASK CONTEXT
{task_context}

### OTHER TASKS (DO NOT COVER)
{other_tasks_block}

### EXISTING TASK TEST CASES (JSON)
{existing_cases_json}
""".strip()


def build_task_patch_prompt(
    task_id: str,
    task_name: str,
    story_summary: str,
    acceptance_block: str,
    task_context: str,
    other_tasks_block: str,
    existing_cases_json: str,
    audit_payload_json: str,
) -> str:
    return f"""
You are a QA engineer. Add ONLY missing test cases for the task based on the audit report.

RULES:
- Add only cases supported by the acceptance criteria listed below.
- Use Positive 30-40%, Negative 25-35%, Edge 20-25%, Integration 15-20% only as approximate mix guidance. Never add an unsupported or duplicate patch case merely to approach a percentage.
- Every returned case must reference only AC IDs listed below.
- Do not invent behavior or cover another task.
- Generate atomic cases with exactly one condition and one expected outcome.
- Do not combine two validation failures or two independent checks in one testcase.
- Each returned testcase must reference exactly one AC ID.
- The referenced AC must directly describe the behavior being tested; do not map a case to a nearby AC from the same task.
- `expected` must be one string, never an array or object.
- Preconditions are setup only; steps are executable actions only; outcomes belong only in `expected`.
- Do not add a constraint or failure behavior absent from the listed AC text or structured assertions.
- Do not introduce a screen, tool, channel, access method, data source, user role, message text, or verification mechanism unless it appears in the current task or mapped AC text.
- Do not copy the acceptance criterion text verbatim as the testcase title, step, or expected result.
- Use at least two concrete chronological steps whenever interaction is required.
- Use Negative for cancellation, blocked login attempts, invalid sessions, denied access, or prevented actions.
- Use Integration for cross-browser, cross-device, previous-session replacement, persisted session state, or multi-client behavior.
- Use Edge for explicit limits such as "only one", "at a time", "exactly", "maximum", or "minimum".
- Every returned testcase must use the key `expected`; never use `expectedResult`.
- Return JSON only. No markdown, no code fences, no commentary.
- The response MUST start with {{ and end with }}.
- Do not add paraphrase duplicates. If a candidate tests the same condition and same outcome as an existing case, omit it.
- Only emit Edge or Integration when the audit explicitly requires that scenario and the AC supports it.
- Make each step concrete and executable; never use generic placeholder wording.
- Return steps in chronological dependency order. A page/control must be opened or displayed before any step clicks, selects, enters, or inspects it.
- Do NOT include any text before or after the JSON object.
- Do NOT wrap the JSON in ```json fences.

JSON SCHEMA:
{{
  "taskId": "{task_id}",
  "taskName": "{task_name}",
  "testCases": [
    {{
      "id": "TC{task_id}.X",
      "title": "<case title>",
      "scenarioType": "Positive | Negative | Edge | Integration",
      "preconditions": ["..."],
      "steps": ["..."],
      "expected": "...",
      "refs": ["AC1"]
    }}
  ]
}}

### STORY SUMMARY
{story_summary}

### ACCEPTANCE CRITERIA INDEX
{acceptance_block}

### TASK CONTEXT
{task_context}

### OTHER TASKS (DO NOT COVER)
{other_tasks_block}

### EXISTING TASK TEST CASES (JSON)
{existing_cases_json}

### AUDIT GAPS (JSON)
{audit_payload_json}
""".strip()


def build_single_task_repair_prompt(
    task_index: int,
    task_name: str,
    story_ctx: str,
    acceptance_block: str,
    derived_block: str,
    task_ctx: str,
    existing_summary: str,
    missing_list: str,
    ref_note: str,
) -> str:
    return f"""
You are fixing gaps for a single task's testcase suite.

STRICT RULES:
- Markdown only. No code fences. No commentary.
- Output ONLY additional test cases for Task {task_index}.
- Do NOT repeat any existing test cases.
- Add ONLY what is needed.
- Scenario types needed: {missing_list}
- {ref_note}

### STORY SUMMARY
{story_ctx}

### ACCEPTANCE CRITERIA INDEX
{acceptance_block}

### DERIVED REQUIREMENTS INDEX (R#)
{derived_block}

### TASK CONTEXT
Task {task_index}: {task_name}
{task_ctx}

### EXISTING TASK SUITE (COMPRESSED)
{existing_summary}

OUTPUT FORMAT:
### Task {task_index} – {task_name}

#### Test Case <temporary id ok> – <Case title>
- **Scenario Type:** Positive | Negative | Edge | Integration
- **Preconditions:** ...
- **Steps:**
  1. ...
- **Expected:** ...
- **Coverage Notes:** ... Refs: [AC1, R2]
""".strip()


def build_task_markdown_prompt(
    title: str,
    remediation: str,
    story_compact: str,
    acceptance_block: str,
    derived_block: str,
    breakdown_compact: str,
) -> str:
    return f"""
You are a principal QA architect. Convert each implementation task into a balanced manual test suite that fully satisfies the acceptance criteria.
{remediation}

### VALIDATED USER STORY (MARKDOWN)
{story_compact}

### ACCEPTANCE CRITERIA INDEX
{acceptance_block}

### DERIVED REQUIREMENTS INDEX (R#)
{derived_block}

### TASK BREAKDOWN MARKDOWN
{breakdown_compact}

RESPONSE RULES:
1. Use markdown only. No HTML, no code fences, no commentary outside the structure.
2. Preserve original task numbering (Task 1, Task 2, ...).
3. For each task, prefer this overall mix when supported by the mapped criteria: Positive 30-40%, Negative 25-35%, Edge 20-25%, Integration 15-20%. Do not force every scenario type into every task.
4. Each test case must follow this structure exactly:
   #### Test Case TC<taskIndex>.<sequence> – <Case title>
   - **Scenario Type:** Positive | Negative | Edge | Integration
   - **Preconditions:** <state, data, or feature flags>
   - **Steps:**
     1. Step detail
     2. Next step
   - **Expected:** <single measurable outcome>
   - **Coverage Notes:** <risk, data set, or persona>. Refs: [AC#, AC#]
5. Reference acceptance criteria by ID (AC1, AC2, …) inside every Coverage Notes entry. If an AC is not covered yet, create a focused test for it.
5b. Also reference derived requirements by ID (R1, R2, …) where applicable.
6. Insert blank lines between headings and major sections for readability.
7. After enumerating all tasks, append a `### Scenario Assurance Checklist` summarizing scenario counts per task and confirming that every AC is referenced.

TEMPLATE (repeat per task):
## TASK TEST CASES — {title}

### Task 1 – <Task Name>

#### Test Case TC1.1 – <Case title>
- **Scenario Type:** Positive
- **Preconditions:** <context>
- **Steps:**
  1. ...
  2. ...
- **Expected:** ...
- **Coverage Notes:** ... Refs: [AC1]

#### Test Case TC1.2 – <Case title>
- ...

### Scenario Assurance Checklist
- Task 1: Positive/Negative/Edge/Integration counts follow the mapped ACs and approximate story-level mix.
- Criteria Alignment: AC1, AC2, AC3 all referenced
""".strip()


def build_single_task_prompt(
    task_index: int,
    task_name: str,
    story_ctx: str,
    acceptance_block: str,
    derived_block: str,
    task_ctx: str,
) -> str:
    return f"""
You are a principal QA architect. Generate exhaustive manual test cases ONLY for the task below.

STRICT RULES:
- Markdown only. No HTML. No code fences. No commentary.
- Output ONLY the section for this task (start with `### Task {task_index} – ...`).
- Produce only scenario types supported by this task's mapped acceptance criteria. Prefer the story-level mix Positive 30-40%, Negative 25-35%, Edge 20-25%, Integration 15-20% when applicable.
- Every test case MUST include `Coverage Notes` with `Refs: [AC#, R#]`.

### STORY SUMMARY
{story_ctx}

### ACCEPTANCE CRITERIA INDEX
{acceptance_block}

### DERIVED REQUIREMENTS INDEX (R#)
{derived_block}

### TASK CONTEXT
Task {task_index}: {task_name}
{task_ctx}

OUTPUT FORMAT:
### Task {task_index} – {task_name}

#### Test Case TC{task_index}.1 – <Case title>
- **Scenario Type:** Positive | Negative | Edge | Integration
- **Preconditions:** ...
- **Steps:**
  1. ...
- **Expected:** ...
- **Coverage Notes:** ... Refs: [AC1, R2]
""".strip()


def build_story_summary_prompt(compact: str) -> str:
    return f"""
Summarize the user story for QA testcase generation.

Rules:
- Output plain text only.
- Max 10 bullets.
- Include: actors/roles, main flow, key validations, integrations/dependencies, error handling expectations.
- Do not invent scope.

STORY (MARKDOWN):
{compact}
""".strip()


def build_repair_prompt(
    title: str,
    story_compact: str,
    breakdown_compact: str,
    acceptance_block: str,
    derived_block: str,
    existing_summary: str,
    missing_req_block: str,
    missing_scenario_block: str,
) -> str:
    return f"""
You are fixing gaps in an existing QA testcase suite. Output ONLY additional test cases to close the missing coverage.

STRICT RULES:
- Markdown only. No code fences. No commentary.
- Do NOT repeat existing test cases.
- Add ONLY what is needed to cover the missing requirement IDs and missing scenario types.
- Every new test case MUST include Coverage Notes with Refs: [AC#, R#].
- Ensure scenario types match the missing list (Positive/Negative/Edge/Integration).

TARGET TITLE: {title}

### USER STORY (MARKDOWN)
{story_compact}

### TASK BREAKDOWN (MARKDOWN)
{breakdown_compact}

### REQUIREMENTS INDEX
Acceptance Criteria:
{acceptance_block}

Derived Requirements:
{derived_block}

### EXISTING TEST CASES (MARKDOWN)
{existing_summary}

MISSING REQUIREMENT IDS:
{missing_req_block}

MISSING SCENARIO TYPES BY TASK (JSON):
{missing_scenario_block}

OUTPUT FORMAT:
### Task <N> – <Task Name>

#### Test Case <temporary id ok> – <Case title>
- **Scenario Type:** Positive | Negative | Edge | Integration
- **Preconditions:** ...
- **Steps:**
  1. ...
- **Expected:** ...
- **Coverage Notes:** ... Refs: [AC1, R2]
""".strip()


def build_acceptance_coverage_addendum_prompt(
    story_summary: str,
    acceptance_block: str,
    missing_block: str,
) -> str:
    return f"""
You are a senior QA engineer. Add ONLY the missing acceptance-criteria test cases listed below.

STRICT RULES:
- Markdown only. No HTML. No code fences. No commentary.
- Output ONLY the section for Task 0 (Acceptance Criteria Coverage).
- Create at least TWO test cases per missing AC (Positive + Negative). Add Edge or Integration if applicable.
- Every test case MUST include Coverage Notes with Refs: [AC#].

### STORY SUMMARY
{story_summary}

### ACCEPTANCE CRITERIA INDEX
{acceptance_block}

MISSING ACCEPTANCE IDS:
{missing_block}

OUTPUT FORMAT:
### Task 0 – Acceptance Criteria Coverage

#### Test Case TC0.1 – <Case title>
- **Scenario Type:** Positive | Negative | Edge | Integration
- **Preconditions:** ...
- **Steps:**
  1. ...
- **Expected:** ...
- **Coverage Notes:** ... Refs: [AC1]
""".strip()


def build_acceptance_coverage_addendum_json_prompt(
    story_summary: str,
    acceptance_block: str,
    missing_block: str,
) -> str:
    return f"""
You are a senior QA engineer. Add ONLY the missing acceptance-criteria test cases listed below.

STRICT RULES:
- Return JSON only. No markdown, no code fences, no commentary.
- The response MUST start with {{ and end with }}.
- Do NOT include any text before or after the JSON object.
- Do NOT wrap the JSON in ```json fences.
- Create at least TWO test cases per missing AC (Positive + Negative). Add Edge or Integration if applicable.
- Every test case MUST include refs with AC# in `refs`.

JSON SCHEMA:
{{
  "taskId": "T0",
  "taskName": "Acceptance Criteria Coverage",
  "testCases": [
    {{
      "id": "TC0.1",
      "title": "<case title>",
      "scenarioType": "Positive | Negative | Edge | Integration",
      "preconditions": ["..."],
      "steps": ["..."],
      "expected": "...",
      "refs": ["AC1"]
    }}
  ]
}}

### STORY SUMMARY
{story_summary}

### ACCEPTANCE CRITERIA INDEX
{acceptance_block}

MISSING ACCEPTANCE IDS:
{missing_block}
""".strip()


story_expansion_prompt = """
You are a Senior Business Analyst and QA Architect.
Your task is to EXPAND, CLARIFY, and NORMALIZE the given user story so that it is:

- Unambiguous
- Complete
- Explicit
- Ready for granular task and test case generation


IMPORTANT THINKING RULES (INTERNAL ONLY):
Before writing the output, you MUST internally:

1. Identify implicit requirements ONLY within the stated scope
2. Identify missing validations for the mentioned features only
3. Identify assumptions a developer or QA might make about the stated functionality
4. Identify system behaviors not explicitly stated BUT directly related to mentioned features
5. Resolve ambiguities by making reasonable, conservative assumptions

DO NOT output your reasoning or explanations.
ONLY output the final expanded user story as valid JSON.

---

### INPUT USER STORY

Title:

{title}

Description:

{description}

Acceptance Criteria:

{acceptance_criteria}

---

### EXPANSION RULES

- Preserve original intent
- Do NOT invent unrelated features
- Convert vague phrases into explicit behaviors
- Make validations, conditions, and outcomes explicit
- Expand acceptance criteria into detailed, testable statements
- Assume a real production system (not a demo)

---

CRITICAL INSTRUCTION:

- Do not include any explanatory text, reasoning, or comments
- Do not wrap the JSON in markdown code blocks (```json```)
- Your response must START with { and END with }
- Return ONLY valid JSON

### OUTPUT FORMAT (STRICT)

Return ONLY valid JSON.

{
  "expandedUserStory": {
    "summary": "<Clear, expanded summary>",
    "detailedDescription": [
      "<Expanded functional behavior 1>",
      "<Expanded functional behavior 2>"
    ],
    "expandedAcceptanceCriteria": [
      "<Explicit, testable acceptance criterion 1>",
      "<Explicit, testable acceptance criterion 2>"
    ],
    "assumptions": [
      "<Assumption made to remove ambiguity>"
    ],
    "outOfScope": [
      "<Explicitly excluded behavior if any>"
    ]
  }
}
"""

task_breakdown_prompt = """
You are a QA Lead specializing in requirement decomposition.

Your task is to break the expanded user story into ATOMIC TASKS.
Each task must represent:
- One behavior
- One validation
- One rule
- Or one system interaction

⚠️ INTERNAL THINKING RULES (DO NOT OUTPUT):
1. Read every acceptance criterion carefully
2. Identify all actions, validations, conditions, and outcomes
3. Split compound behaviors into separate tasks
4. Ensure tasks are small enough to be independently testable

DO NOT output your reasoning.

---

### INPUT
Expanded User Story:
{expanded_user_story_json}

---

### TASK DECOMPOSITION RULES

- Tasks must be granular (no combined logic)
- Tasks must be testable independently
- Tasks must be traceable to acceptance criteria
- Do NOT skip validations or error handling

---

### OUTPUT FORMAT (STRICT JSON)

{
  "tasks": [
    {
      "taskId": "TASK-001",
      "taskDescription": "<Atomic behavior or rule>",
      "relatedAcceptanceCriteria": [
        "<AC reference or text>"
      ]
    }
  ]
}

"""

test_case_generation_prompt = """

You are a Senior QA Engineer with strong experience in manual testing, automation readiness, and enterprise QA standards.

Your responsibility is to generate DETAILED, EXECUTABLE test cases for EXACTLY ONE atomic task.

You must think like a real QA engineer validating production-grade software.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INTERNAL THINKING RULES (DO NOT OUTPUT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Before writing the test cases, you MUST internally perform the following steps:

1. Understand the Task Precisely
   - Identify what behavior is being validated
   - Identify inputs, system actions, and outputs
   - Identify validations and failure conditions

2. Identify Test Scenarios
   - At least one positive scenario
   - At least one negative scenario
   - At least one edge or boundary scenario (if applicable)

3. Apply QA Design Techniques
   - Equivalence Partitioning
   - Boundary Value Analysis (if applicable)
   - Negative Testing
   - Data Validation

4. Define Observable Outcomes
   - UI messages
   - API responses
   - System state changes

DO NOT output your reasoning or analysis.
Only output the final test cases.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INPUT CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Expanded User Story:
{expanded_user_story_json}

Atomic Task:
{
  "taskId": "{task_id}",
  "taskDescription": "{task_description}",
  "relatedAcceptanceCriteria": {related_acceptance_criteria}
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT TEST CASE GENERATION RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Each test case MUST:
- Validate ONLY the given task
- Be specific and non-generic
- Use realistic, varied test data
- Be executable without assumptions

testSteps MUST:
- Contain at least 4 steps
- Clearly specify:
  - User/system action
  - Target field/button/API
  - Exact data used

expectedResult MUST:
- Be a single, precise, observable outcome
- Mention exact system behavior (message, response, state)

NOT ALLOWED:
- Vague phrases (e.g., "Verify functionality works")
- Skipping validations
- Combining multiple tasks into one test case
- Reusing identical data across all test cases

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT (STRICT JSON ONLY)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Return ONLY valid JSON.
NO markdown.
NO explanations.
NO extra text.

{
  "taskId": "{task_id}",
  "testCases": [
    {
      "testCaseId": "TC-{task_id}-001",
      "testDescription": "<Specific validation performed>",
      "testSteps": [
        "<Step 1: concrete action with data>",
        "<Step 2>",
        "<Step 3>",
        "<Step 4>"
      ],
      "expectedResult": "<Exact, observable outcome>"
    }
  ]
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUALITY EXPECTATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Generate MULTIPLE test cases for this task
- Cover:
  - Positive scenario
  - Negative scenario
  - Edge or boundary scenario
- Ensure test cases can be directly automated if needed

Generate test cases for the given task now.
"""

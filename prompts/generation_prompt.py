from models.requirement import Requirement


class GenerationPromptBuilder:
    """
    Builds the QA Boat generation prompt.

    NOTE:
    This prompt intentionally matches the Cognine QA Boat prompt.
    The ONLY modification is replacing Azure DevOps task details
    with Requirement details parsed from our Excel workbook.
    """

    @staticmethod
    def build(requirement: Requirement) -> str:

        return f"""You are an expert QA engineer. Your response MUST be ONLY valid JSON with NO additional text.
 
CRITICAL INSTRUCTIONS:
- Your response MUST start with {{ and end with }}
- NO introductory text like "Here is the JSON output:"
- NO markdown code blocks (no ```json or ```)
- NO explanations before or after the JSON
- NO comments inside the JSON
- Output ONLY the raw JSON object
- You MUST analyze the task details and generate REAL test cases, NOT placeholder examples
 
--- REQUIREMENT DETAILS ---

Requirement ID:
{requirement.requirement_id}

Requirement Type:
{requirement.requirement_type}

Title:
{requirement.title}

Description / Acceptance Criteria:
{requirement.description}

Business Rules:
{requirement.business_rules}

Priority:
{requirement.priority}
 
--- YOUR TASK ---
Analyze the requirement details above and generate realistic, thorough test cases that validate the specific functionality described.
 
--- REQUIRED JSON SCHEMA ---
 
Return a JSON object matching this EXACT structure.
IMPORTANT: Replace ALL placeholder values with ACTUAL test cases based on the requirement above.
DO NOT return these placeholder values - generate real test cases specific to the requirement.
 
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
   - Must be directly related to the requirement
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
 
1. ANALYZE THE REQUIREMENT: Read the Description / Acceptance Criteria carefully.
2. GENERATE MULTIPLE TEST CASES: Create at least 5-10 test cases covering:
   - Positive scenarios (happy path)
   - Negative scenarios (error cases, invalid inputs)
   - Edge cases (boundary conditions, empty fields, special characters)
   - Integration scenarios (if applicable)
 
3. MAP TO ACCEPTANCE CRITERIA: Each acceptance criterion should have at least one corresponding test case.
 
4. BE SPECIFIC: Test cases must be directly relevant to the requirement, not generic examples.
 
5. USE REALISTIC DATA: Reference actual fields, buttons, and features mentioned in the requirement.
 
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
- DO analyze the requirement and create relevant test cases
- DO ensure test cases directly address the requirement
 
YOUR RESPONSE MUST START WITH {{ AND END WITH }}
 
Analyze the requirement above and generate specific test cases now:"""
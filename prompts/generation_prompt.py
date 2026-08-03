from models.requirement import Requirement


class GenerationPromptBuilder:
    """
    Builds prompts for LLM-based software test case generation.
    This prompt is shared by QA Boat, Ollama models and Gemini.
    """

    @staticmethod
    def build(requirement: Requirement) -> str:

        return f"""
You are an expert Software QA Engineer specializing in Manual Testing,
Automation Testing, API Testing, Integration Testing and Test Design.

Your responsibility is to analyze the business requirement and generate
high-quality, realistic software test cases.

=========================================================
CRITICAL INSTRUCTIONS
=========================================================

• Return ONLY valid JSON.
• Do NOT return Markdown.
• Do NOT use ```json.
• Do NOT explain your response.
• Do NOT add introductory or concluding text.
• Do NOT include comments.
• Response MUST start with '{{'
• Response MUST end with '}}'
• Use ONLY double quotes.
• JSON must be syntactically valid.

=========================================================
BUSINESS REQUIREMENT
=========================================================

Requirement ID:
{requirement.requirement_id}

Module:
{requirement.module}

Title:
{requirement.title}

Description:
{requirement.description}

Acceptance Criteria:
{requirement.acceptance_criteria}

Business Rules:
{requirement.business_rules}

Priority:
{requirement.priority}

=========================================================
YOUR TASK
=========================================================

Generate realistic software test cases.

Cover all applicable scenarios including:

• Positive Scenarios
• Negative Scenarios
• Boundary Value Testing
• Edge Cases
• Validation Checks
• Error Handling
• Business Rule Validation

Use appropriate software testing techniques whenever applicable.

Examples include:

• Boundary Value Analysis
• Equivalence Partitioning
• Decision Table Testing
• State Transition Testing
• Error Guessing

Generate between 5 and 15 meaningful test cases.

Every Acceptance Criteria must have at least one mapped test case.

Do NOT generate duplicate test cases.

Do NOT invent functionality that does not exist.

Generate realistic business test data.

=========================================================
OUTPUT JSON SCHEMA
=========================================================

Return ONLY valid JSON.

{{
  "requirement": {{
      "requirementId": "{requirement.requirement_id}",
      "title": "{requirement.title}"
  }},

  "coverageSummary": {{

      "acceptanceCriteriaCovered": [

          {{
              "id": "AC1",
              "text": "Acceptance Criteria"
          }}

      ],

      "coveredTestTypes": [

          "Positive",
          "Negative",
          "Boundary",
          "Edge",
          "Validation"

      ],

      "coveredTestTechniques": [

          "Boundary Value Analysis",
          "Equivalence Partitioning"

      ]
  }},

  "executionContext": {{

      "entryCriteria": [

          "Application is available",

          "Required test data exists"

      ],

      "exitCriteria": [

          "Expected business behaviour verified"

      ]

  }},

  "testCases":[

      {{

          "testCaseId":"TC001",

          "acceptanceCriteriaRef":[

              {{
                  "id":"AC1",
                  "text":"Acceptance Criteria"
              }}

          ],

          "testType":"Positive",

          "testTechnique":"Equivalence Partitioning",

          "priority":"High",

          "riskLevel":"High",

          "testDescription":"Validate successful execution.",

          "testData":{{
              "field":"value"
          }},

          "testSteps":[

              "Step 1",

              "Step 2"

          ],

          "expectedResult":"Expected business behaviour."
      }}

  ]

}}

=========================================================
VALIDATION RULES
=========================================================

The response MUST satisfy ALL the following:

• Valid JSON
• No Markdown
• No explanations
• No comments
• Every testCaseId must be unique
• Every Acceptance Criteria must have at least one mapped test case
• testSteps must contain at least two steps
• expectedResult must not be empty
• testData must contain realistic values
• No duplicate test cases

Allowed Test Types

• Positive
• Negative
• Boundary
• Edge
• Validation

Allowed Test Techniques

• Boundary Value Analysis
• Equivalence Partitioning
• Decision Table Testing
• State Transition Testing
• Error Guessing

Priority

• High
• Medium
• Low

Risk Level

• High
• Medium
• Low

Return ONLY the JSON object.
"""
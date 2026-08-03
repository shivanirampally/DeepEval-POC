from models.requirement import Requirement
from prompts.generation_prompt import GenerationPromptBuilder

requirement = Requirement(
    requirement_id="R001",
    module="Login",
    title="User Login",
    description="User should be able to login with valid credentials.",
    acceptance_criteria="""
AC1: User can login with valid username and password.
AC2: Error should be shown for invalid credentials.
""",
    business_rules="Password is mandatory.",
    priority="High"
)

prompt = GenerationPromptBuilder.build(requirement)

print(prompt)
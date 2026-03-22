from app.llm_provider import generate_response
from app.schemas import Plan
import json

def clean_json_response(response: str) -> str:
    response = response.strip()

    # Remove markdown code blocks
    if response.startswith("```"):
        response = response.split("```")[1]  # remove first ```
        if response.startswith("json"):
            response = response[4:]  # remove 'json'
    
    if response.endswith("```"):
        response = response[:-3]

    return response.strip()

def create_plan(user_query: str, feedback: str = None, max_retries: int = 3):
    prompt = f"""
You are an AI planner.

Break the user query into step-by-step actions.

STRICT RULES:
- Return ONLY valid JSON
- No markdown
- tool_input must ALWAYS be a string

Format:
{{
  "steps": [
    {{
      "step_number": 1,
      "action": "...",
      "tool_name": "...",
      "tool_input": "..."
    }}
  ]
}}

User Query:
{user_query}
"""

    if feedback:
        prompt += f"""\n\nFeedback from previous attempt: {feedback}
        
        Improve the plan by fixing these issues.
        """

    for attempt in range(max_retries):
        response = generate_response(prompt)
        cleaned = clean_json_response(response)

        try:
            plan_dict = json.loads(cleaned)
            plan = Plan(**plan_dict)
            return plan

        except Exception as e:
            print(f"Attempt {attempt+1} failed:", e)
    return None
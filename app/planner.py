from app.llm_provider import generate_response
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

def create_plan(user_query: str):
    prompt = f"""
You are an AI planner.

Break the user query into step-by-step actions.

IMPORTANT:
- tool_input must ALWAYS be a string
- Do NOT return dictionaries inside tool_input

Return ONLY valid JSON.

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

    response = generate_response(prompt)
    cleaned = clean_json_response(response)
    try:
        plan_json = json.loads(cleaned)
        return plan_json
    except Exception as e:
        print("Error parsing plan:", e)
        print("Error response:", cleaned)
        print("Error response:", response)
        return None
from app.llm_provider import generate_response
from app.schemas import CriticResponse
import json

def clean_json_response(response: str) -> str:
    response = response.strip()

    if response.startswith("```"):
        response = response.split("```")[1]
        if response.startswith("json"):
            response = response[4:]

    if response.endswith("```"):
        response = response[:-3]

    return response.strip()

def evaluate_plan(plan, max_retries: int = 3):
    prompt = f"""
    You are an AI critic.

    Evaluate the following plan.

    STRICT RULES:
    - Return ONLY valid JSON
    - No markdown or explanations
    - score must be between 0 and 1
    - issues must be a list of strings
    - suggestions must be a list of strings

    Format:
    {{
    "score": 0.0,
    "issues": [],
    "suggestions": []
    }}

    Plan:
    {plan}
    """

    for attempt in range(max_retries):
        response = generate_response(prompt)
        cleaned = clean_json_response(response)

        try:
            critic_dict = json.loads(cleaned)
            critic = CriticResponse(**critic_dict)
            return critic

        except Exception as e:
            print(f"Critic attempt {attempt+1} failed:", e)

    return None
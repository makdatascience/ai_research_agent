from pydantic import BaseModel
from typing import List

class PlanStep(BaseModel):
    step_number: int
    action: str
    tool_name: str
    tool_input: str

class Plan(BaseModel):
    steps: List[PlanStep]

class CriticResponse(BaseModel):
    score: float
    issues: List[str]
    suggestions: List[str]
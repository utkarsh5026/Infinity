from typing import Optional, Dict, List
from datetime import datetime
from pydantic import BaseModel, Field


class ExplanationRequest(BaseModel):
    card_id: str
    session_id: Optional[str] = None


class ExplanationResponse(BaseModel):
    id: str
    card_id: str
    explanation: str
    generated_at: str
    refinement_count: int
    user_level: int
    metadata: Dict


class RefinementRequest(BaseModel):
    explanation_id: str
    refinement_request: str = Field(
        ...,
        max_length=200,
        description="User's request for refinement (e.g., 'make it simpler', 'more examples')"
    )


class RefinementHistory(BaseModel):
    request: str
    type: str
    timestamp: str


class RefinementResponse(BaseModel):
    id: str
    card_id: str
    explanation: str
    generated_at: str
    refinement_count: int
    user_level: int
    metadata: Dict
    last_refined_at: Optional[str] = None
    refinement_history: Optional[List[RefinementHistory]] = []
    refinement_applied: bool = True

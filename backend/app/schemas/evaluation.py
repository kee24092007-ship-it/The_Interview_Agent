"""Evaluation request/response schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EvaluationCreate(BaseModel):
    session_id: int
    answer_id: int | None = None
    score: float = Field(default=0.0, ge=0, le=10)
    communication_score: float | None = Field(default=None, ge=0, le=10)
    technical_score: float | None = Field(default=None, ge=0, le=10)
    feedback: str | None = None
    strengths: str | None = None
    improvements: str | None = None
    raw_ai_payload: str | None = None


class EvaluationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    answer_id: int | None
    score: float
    communication_score: float | None
    technical_score: float | None
    feedback: str | None
    strengths: str | None
    improvements: str | None
    raw_ai_payload: str | None
    created_at: datetime

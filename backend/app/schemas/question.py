"""Question request/response schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import Difficulty, QuestionType


class QuestionBase(BaseModel):
    session_id: int
    content: str = Field(..., min_length=1)
    question_type: QuestionType = QuestionType.behavioral
    difficulty: Difficulty = Difficulty.medium
    order: int = 0


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class QuestionGenerateRequest(BaseModel):
    """Request to have the AI generate a bank of interview questions."""

    job_title: str
    job_description: str | None = None
    candidate_skills: str | None = None
    count: int = Field(default=8, ge=1, le=25)
    question_types: list[QuestionType] = Field(
        default_factory=lambda: [
            QuestionType.behavioral,
            QuestionType.technical,
            QuestionType.situational,
        ]
    )

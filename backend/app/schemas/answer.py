"""Answer request/response schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AnswerCreate(BaseModel):
    session_id: int
    question_id: int
    text: str | None = None
    transcript: str | None = None
    audio_url: str | None = None
    duration_seconds: int | None = Field(default=None, ge=0)


class AnswerUpdate(BaseModel):
    text: str | None = None
    transcript: str | None = None
    audio_url: str | None = None
    duration_seconds: int | None = Field(default=None, ge=0)


class AnswerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    question_id: int
    text: str | None
    transcript: str | None
    audio_url: str | None
    duration_seconds: int | None
    created_at: datetime

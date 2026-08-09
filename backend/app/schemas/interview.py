"""Schemas for the interview flow endpoint."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class InterviewPayload(BaseModel):
    sessionId: str = Field(..., min_length=1)
    candidate: dict[str, Any] | None = None
    message: str | None = None


class FeedbackPayload(BaseModel):
    summary: str
    strengths: list[str]
    gaps: list[str]
    next: list[str]


class InterviewResponse(BaseModel):
    reply: str
    done: bool
    feedback: FeedbackPayload | None = None

"""InterviewSession request/response schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import SessionStatus


class SessionBase(BaseModel):
    candidate_id: int
    job_title: str = Field(..., min_length=1, max_length=255)
    job_description: str | None = None
    status: SessionStatus = SessionStatus.scheduled


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    job_title: str | None = Field(default=None, min_length=1, max_length=255)
    job_description: str | None = None
    status: SessionStatus | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None


class SessionRead(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    started_at: datetime | None
    ended_at: datetime | None
    created_at: datetime

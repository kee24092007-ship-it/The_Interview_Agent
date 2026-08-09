"""Interview flow state for the single `/api/interview` endpoint."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class InterviewFlow(Base):
    """Persistent state for an interview session driven by sessionId."""

    __tablename__ = "interview_flows"

    session_id: Mapped[str] = mapped_column(String(100), primary_key=True, index=True)
    candidate_data: Mapped[str] = mapped_column(Text, nullable=False)
    answers: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    current_question: Mapped[int] = mapped_column(Integer, default=0)
    stage: Mapped[str] = mapped_column(String(30), default="welcome", index=True)
    status: Mapped[str] = mapped_column(String(30), default="active", index=True)
    feedback_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    feedback_strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    feedback_gaps: Mapped[str | None] = mapped_column(Text, nullable=True)
    feedback_next: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )

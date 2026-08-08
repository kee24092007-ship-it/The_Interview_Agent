"""Evaluation ORM model - AI-generated scoring and feedback."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _grade_default() -> float:
    return 0.0


class Evaluation(Base):
    """An AI evaluation of either a single answer or an entire session.

    If answer_id is set, this evaluation pertains to that specific answer;
    otherwise it is a session-level overall evaluation.
    """

    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id", ondelete="CASCADE"), index=True)
    answer_id: Mapped[int | None] = mapped_column(ForeignKey("answers.id", ondelete="CASCADE"), nullable=True, index=True)

    # Scores are 0.0 - 10.0 unless otherwise noted.
    score: Mapped[float] = mapped_column(Float, default=_grade_default)
    communication_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    technical_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    improvements: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_ai_payload: Mapped[str | None] = mapped_column(Text, nullable=True)  # full JSON from the AI for audit
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())

    session: Mapped["InterviewSession"] = relationship(back_populates="evaluations")  # noqa: F821
    answer: Mapped["Answer | None"] = relationship()  # noqa: F821

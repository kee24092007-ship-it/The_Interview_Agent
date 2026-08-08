"""InterviewSession ORM model - one interview run for a candidate and a role."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class InterviewSession(Base):
    """A single interview session linking a candidate with a target role."""

    __tablename__ = "interview_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True)

    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    job_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # scheduled | in_progress | completed | cancelled
    status: Mapped[str] = mapped_column(String(50), default="scheduled", index=True)

    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())

    candidate: Mapped["Candidate"] = relationship(back_populates="sessions")  # noqa: F821
    questions: Mapped[list["Question"]] = relationship(  # noqa: F821
        back_populates="session", cascade="all, delete-orphan", order_by="Question.id"
    )
    evaluations: Mapped[list["Evaluation"]] = relationship(  # noqa: F821
        back_populates="session", cascade="all, delete-orphan"
    )

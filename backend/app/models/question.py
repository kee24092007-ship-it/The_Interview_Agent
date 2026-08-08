"""Question ORM model - an interview question asked within a session."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Question(Base):
    """An interview question belonging to a session.

    question_type is one of: behavioral, technical, coding, situational,
    strengths, custom.
    """

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id", ondelete="CASCADE"), index=True)

    content: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(50), default="behavioral", index=True)
    difficulty: Mapped[str] = mapped_column(String(20), default="medium")  # easy | medium | hard
    order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())

    session: Mapped["InterviewSession"] = relationship(back_populates="questions")  # noqa: F821
    answer: Mapped["Answer | None"] = relationship(  # noqa: F821
        back_populates="question", uselist=False, cascade="all, delete-orphan"
    )

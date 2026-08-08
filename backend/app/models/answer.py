"""Answer ORM model - a candidate's response to a question."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Answer(Base):
    """A candidate's answer to a single question within a session.

    The answer may be recorded as free-form text and/or a reference to an
    uploaded audio/video recording (transcript is stored separately when
    speech-to-text is enabled).
    """

    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id", ondelete="CASCADE"), index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), index=True, unique=True)

    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)  # speech-to-text output
    audio_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), server_default=func.now())

    session: Mapped["InterviewSession"] = relationship()  # noqa: F821
    question: Mapped["Question"] = relationship(back_populates="answer")  # noqa: F821

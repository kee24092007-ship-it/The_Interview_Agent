"""CRUD routes for interview sessions, including AI question generation."""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.candidate import Candidate
from app.models.question import Question
from app.models.session import InterviewSession
from app.schemas.question import QuestionGenerateRequest, QuestionRead
from app.schemas.session import SessionCreate, SessionRead, SessionUpdate
from app.services import ai

router = APIRouter(prefix="/sessions", tags=["sessions"])


_FALLBACK_QUESTIONS = [
    ("Explain the most important technical concept you would use in this role.", "technical", "medium"),
    ("Walk me through a project you built and the engineering decisions you made.", "technical", "medium"),
    ("How would you debug an API that works locally but fails in production?", "situational", "hard"),
    ("How would you design a reliable API between a frontend and backend?", "technical", "medium"),
    ("Describe a difficult technical problem and how you approached solving it.", "behavioral", "medium"),
    ("How would you test a new feature before deploying it to production?", "technical", "medium"),
    ("What trade-offs would you consider when choosing an AI model for a production system?", "technical", "hard"),
    ("How would you monitor and improve an AI application after deployment?", "technical", "hard"),
]


def _safe_generated_questions(generated: object, count: int) -> list[dict[str, object]]:
    """Normalize AI output so invalid model JSON can never break the API response."""
    allowed_types = {"behavioral", "technical", "coding", "situational", "strengths", "custom"}
    allowed_difficulties = {"easy", "medium", "hard"}
    safe: list[dict[str, object]] = []

    if isinstance(generated, list):
        for item in generated:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if not isinstance(content, str) or not content.strip():
                continue
            qtype = item.get("question_type")
            difficulty = item.get("difficulty")
            safe.append(
                {
                    "content": content.strip(),
                    "question_type": qtype if qtype in allowed_types else "technical",
                    "difficulty": difficulty if difficulty in allowed_difficulties else "medium",
                    "order": len(safe),
                }
            )
            if len(safe) >= count:
                return safe

    # Always return the requested number even if the AI returned malformed or
    # incomplete JSON. This keeps the Question Bank usable without an AI outage.
    for content, qtype, difficulty in _FALLBACK_QUESTIONS:
        if len(safe) >= count:
            break
        safe.append(
            {
                "content": content,
                "question_type": qtype,
                "difficulty": difficulty,
                "order": len(safe),
            }
        )
    return safe[:count]


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session(payload: SessionCreate, db: Session = Depends(get_db)) -> InterviewSession:
    if db.get(Candidate, payload.candidate_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found.")
    session = InterviewSession(**payload.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("", response_model=list[SessionRead])
def list_sessions(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
) -> list[InterviewSession]:
    return list(
        db.scalars(
            select(InterviewSession)
            .order_by(InterviewSession.created_at.desc())
            .limit(limit)
            .offset(offset)
        ).all()
    )


@router.get("/{session_id}", response_model=SessionRead)
def get_session(session_id: int, db: Session = Depends(get_db)) -> InterviewSession:
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    return session


@router.patch("/{session_id}", response_model=SessionRead)
def update_session(session_id: int, payload: SessionUpdate, db: Session = Depends(get_db)) -> InterviewSession:
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(session, field, value)
    db.commit()
    db.refresh(session)
    return session


@router.post("/{session_id}/start", response_model=SessionRead)
def start_session(session_id: int, db: Session = Depends(get_db)) -> InterviewSession:
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    session.status = "in_progress"
    session.started_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(session)
    return session


@router.post("/{session_id}/complete", response_model=SessionRead)
def complete_session(session_id: int, db: Session = Depends(get_db)) -> InterviewSession:
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    session.status = "completed"
    session.ended_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(session)
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, db: Session = Depends(get_db)) -> None:
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    db.delete(session)
    db.commit()


@router.post("/{session_id}/questions/generate", response_model=list[QuestionRead], status_code=status.HTTP_201_CREATED)
def generate_session_questions(
    session_id: int,
    payload: QuestionGenerateRequest,
    db: Session = Depends(get_db),
) -> list[Question]:
    """Generate and persist a valid question set, with a safe local fallback."""
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    try:
        generated = ai.generate_questions(
            job_title=payload.job_title or session.job_title,
            job_description=payload.job_description or session.job_description,
            candidate_skills=payload.candidate_skills,
            count=payload.count,
            question_types=[t.value for t in payload.question_types],
        )
    except Exception:
        # The AI service is expected to fall back itself, but keep this route
        # resilient if a provider/client initialization error escapes it.
        generated = []

    safe_questions = _safe_generated_questions(generated, payload.count)
    created: list[Question] = []
    for item in safe_questions:
        question = Question(
            session_id=session.id,
            content=str(item["content"]),
            question_type=str(item["question_type"]),
            difficulty=str(item["difficulty"]),
            order=int(item["order"]),
        )
        db.add(question)
        created.append(question)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    for question in created:
        db.refresh(question)
    return created

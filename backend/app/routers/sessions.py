"""CRUD routes for interview sessions, including AI question generation."""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
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
def list_sessions(db: Session = Depends(get_db)) -> list[InterviewSession]:
    return list(db.scalars(select(InterviewSession).order_by(InterviewSession.created_at.desc())).all())


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
    """Use the AI to generate questions and persist them to the session."""
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    generated = ai.generate_questions(
        job_title=payload.job_title or session.job_title,
        job_description=payload.job_description or session.job_description,
        candidate_skills=payload.candidate_skills,
        count=payload.count,
        question_types=[t.value for t in payload.question_types],
    )
    created: list[Question] = []
    for item in generated:
        question = Question(
            session_id=session.id,
            content=item["content"],
            question_type=item.get("question_type", "behavioral"),
            difficulty=item.get("difficulty", "medium"),
            order=item.get("order", len(created)),
        )
        db.add(question)
        created.append(question)
    db.commit()
    for question in created:
        db.refresh(question)
    return created

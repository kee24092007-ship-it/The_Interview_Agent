"""CRUD routes for answers, including AI-powered evaluation on submit."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.answer import Answer
from app.models.evaluation import Evaluation
from app.models.question import Question
from app.models.session import InterviewSession
from app.schemas.answer import AnswerCreate, AnswerRead, AnswerUpdate
from app.schemas.evaluation import EvaluationRead
from app.services import ai

router = APIRouter(prefix="/answers", tags=["answers"])


@router.post("", response_model=AnswerRead, status_code=status.HTTP_201_CREATED)
def submit_answer(payload: AnswerCreate, db: Session = Depends(get_db)) -> Answer:
    if db.get(InterviewSession, payload.session_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    question = db.get(Question, payload.question_id)
    if question is None or question.session_id != payload.session_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found for this session.")
    existing = db.scalar(select(Answer).where(Answer.question_id == payload.question_id))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An answer already exists for this question.")
    answer = Answer(**payload.model_dump())
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


@router.get("/session/{session_id}", response_model=list[AnswerRead])
def list_answers_for_session(
    session_id: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
) -> list[Answer]:
    return list(
        db.scalars(select(Answer).where(Answer.session_id == session_id).limit(limit).offset(offset)).all()
    )


@router.get("/{answer_id}", response_model=AnswerRead)
def get_answer(answer_id: int, db: Session = Depends(get_db)) -> Answer:
    answer = db.get(Answer, answer_id)
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found.")
    return answer


@router.patch("/{answer_id}", response_model=AnswerRead)
def update_answer(answer_id: int, payload: AnswerUpdate, db: Session = Depends(get_db)) -> Answer:
    answer = db.get(Answer, answer_id)
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(answer, field, value)
    db.commit()
    db.refresh(answer)
    return answer


@router.post("/{answer_id}/evaluate", response_model=EvaluationRead, status_code=status.HTTP_201_CREATED)
def evaluate_answer(answer_id: int, db: Session = Depends(get_db)) -> Evaluation:
    """Run AI evaluation on the answer and store the resulting evaluation."""
    answer = db.get(Answer, answer_id)
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found.")
    question = db.get(Question, answer.question_id)
    text = answer.text or answer.transcript or ""
    result = ai.evaluate_answer(question.content if question else "", text)
    evaluation = Evaluation(
        session_id=answer.session_id,
        answer_id=answer.id,
        score=float(result.get("score", 0.0)),
        communication_score=result.get("communication_score"),
        technical_score=result.get("technical_score"),
        feedback=result.get("feedback"),
        strengths=result.get("strengths"),
        improvements=result.get("improvements"),
        raw_ai_payload=result.get("raw_ai_payload"),
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(answer_id: int, db: Session = Depends(get_db)) -> None:
    answer = db.get(Answer, answer_id)
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found.")
    db.delete(answer)
    db.commit()

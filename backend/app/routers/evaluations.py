"""CRUD routes for evaluations."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.evaluation import Evaluation
from app.models.session import InterviewSession
from app.schemas.evaluation import EvaluationCreate, EvaluationRead

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.post("", response_model=EvaluationRead, status_code=status.HTTP_201_CREATED)
def create_evaluation(payload: EvaluationCreate, db: Session = Depends(get_db)) -> Evaluation:
    if db.get(InterviewSession, payload.session_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    evaluation = Evaluation(**payload.model_dump())
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation


@router.get("/session/{session_id}", response_model=list[EvaluationRead])
def list_evaluations_for_session(session_id: int, db: Session = Depends(get_db)) -> list[Evaluation]:
    return list(db.scalars(select(Evaluation).where(Evaluation.session_id == session_id)).all())


@router.get("/{evaluation_id}", response_model=EvaluationRead)
def get_evaluation(evaluation_id: int, db: Session = Depends(get_db)) -> Evaluation:
    evaluation = db.get(Evaluation, evaluation_id)
    if evaluation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found.")
    return evaluation


@router.delete("/{evaluation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evaluation(evaluation_id: int, db: Session = Depends(get_db)) -> None:
    evaluation = db.get(Evaluation, evaluation_id)
    if evaluation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation not found.")
    db.delete(evaluation)
    db.commit()

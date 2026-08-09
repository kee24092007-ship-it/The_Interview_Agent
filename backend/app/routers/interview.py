"""Interview flow endpoint for the technical spec."""
from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.interview_flow import InterviewFlow
from app.schemas.interview import FeedbackPayload, InterviewPayload, InterviewResponse

router = APIRouter(prefix="/api/interview", tags=["interview"])

QUESTION_FLOW = [
    "Tell me about your professional background and what motivated you to apply for this role.",
    "What is one project you are most proud of, and what was your specific contribution?",
    "How do you approach troubleshooting a problem when you don't have all the information?",
    "Describe a time you had to learn a new technology quickly. What did you do?",
    "How do you prioritize competing deadlines when working on multiple tasks?",
]


def _build_feedback(interview: InterviewFlow) -> FeedbackPayload:
    strengths = [s for s in (interview.feedback_strengths or "").split("||") if s]
    gaps = [s for s in (interview.feedback_gaps or "").split("||") if s]
    next_points = [s for s in (interview.feedback_next or "").split("||") if s]
    return FeedbackPayload(summary=interview.feedback_summary or "", strengths=strengths, gaps=gaps, next=next_points)


def _deterministic_feedback(messages: list[dict[str, str]]) -> dict[str, list[str] | str]:
    strengths: list[str] = []
    gaps: list[str] = []
    next_points: list[str] = []

    last_answer = messages[-1]["answer"] if messages else ""
    answer_lower = last_answer.lower()

    if len(last_answer.split()) >= 40:
        strengths.append("You provide detailed responses with good structure.")
    else:
        gaps.append("Expand your answers with more concrete examples and outcomes.")

    if any(word in answer_lower for word in ["team", "collaborat", "stakehold", "cross-functional"]):
        strengths.append("You emphasize collaboration and teamwork.")
    else:
        gaps.append("Include more details about how you worked with others.")

    if any(word in answer_lower for word in ["result", "impact", "outcome", "measure"]):
        strengths.append("You focus on results and measurable impact.")
    else:
        next_points.append("Try to mention concrete outcomes or metrics next time.")

    if "learn" in answer_lower or "adapt" in answer_lower:
        strengths.append("You demonstrate a strong learning mindset.")
    else:
        next_points.append("Highlight how you adapt to new tools or processes.")

    summary = "Your interview responses are promising. Continue to prioritize structure, impact, and collaboration in each answer."
    return {
        "summary": summary,
        "strengths": strengths,
        "gaps": gaps,
        "next": next_points,
    }


def _stringify_answers(answers: list[dict[str, str]]) -> str:
    return json.dumps(answers, ensure_ascii=False)


def _parse_answers(raw: str) -> list[dict[str, str]]:
    try:
        return json.loads(raw)
    except ValueError:
        return []


@router.post("", response_model=InterviewResponse)
def handle_interview(
    payload: InterviewPayload,
    db: Session = Depends(get_db),
) -> InterviewResponse:
    if payload.message is None:
        if payload.candidate is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="candidate is required for interview start.")
        existing = db.get(InterviewFlow, payload.sessionId)
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Interview session already exists.")

        interview = InterviewFlow(
            session_id=payload.sessionId,
            candidate_data=json.dumps(payload.candidate, ensure_ascii=False),
            answers=_stringify_answers([]),
            current_question=0,
            stage="active",
            status="active",
        )
        db.add(interview)
        db.commit()
        return InterviewResponse(reply="Welcome. Let's begin your interview.", done=False, feedback=None)

    interview = db.get(InterviewFlow, payload.sessionId)
    if interview is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found.")
    if interview.status != "active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Interview has already completed.")

    answers = _parse_answers(interview.answers)
    current_question_index = min(interview.current_question, len(QUESTION_FLOW) - 1)
    answers.append({"question": QUESTION_FLOW[current_question_index], "answer": payload.message})
    interview.answers = _stringify_answers(answers)
    interview.current_question += 1

    if interview.current_question >= len(QUESTION_FLOW):
        evaluation = _deterministic_feedback(answers)
        interview.status = "completed"
        interview.feedback_summary = evaluation["summary"]
        interview.feedback_strengths = "||".join(evaluation["strengths"])
        interview.feedback_gaps = "||".join(evaluation["gaps"])
        interview.feedback_next = "||".join(evaluation["next"])
        interview.stage = "completed"
        db.commit()
        return InterviewResponse(
            reply="Interview completed.",
            done=True,
            feedback=_build_feedback(interview),
        )

    db.commit()
    next_question = QUESTION_FLOW[interview.current_question]
    return InterviewResponse(reply=next_question, done=False, feedback=None)

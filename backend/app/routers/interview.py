"""Conversational interview endpoint required by the challenge technical spec."""
from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.interview_flow import InterviewFlow
from app.schemas.interview import FeedbackPayload, InterviewPayload, InterviewResponse

router = APIRouter(prefix="/api/interview", tags=["interview"])

QUESTION_BANK: dict[int, tuple[str, list[str]]] = {
    1: ("VS Code & Python Environment Setup", [
        "Why would you use a Python virtual environment, and how does it help a team keep dependencies reproducible?",
        "How would you debug a Python application in VS Code when it works locally but fails in another environment?",
    ]),
    3: ("First AI Project, React Frontend & GitHub", [
        "Walk me through how you would connect a React frontend to a FastAPI backend and handle an API failure gracefully.",
        "What Git workflow would you use to make a feature easy to review and safely integrate into the main branch?",
    ]),
    4: ("Reading & Processing Structured Data", [
        "How would you clean structured CSV data before storing it in SQLite, and what validation would you perform?",
        "When would you use SQL directly instead of processing the same question entirely in application code?",
    ]),
    7: ("Embeddings Explained", [
        "What are text embeddings, and why are they useful in an AI application?",
        "How would you evaluate whether an embedding model is producing useful representations for your retrieval task?",
    ]),
    8: ("Vector Databases Overview", [
        "What problem does a vector database solve in a RAG system, and how is semantic search different from keyword search?",
        "How would you choose between a local Chroma database and a managed vector database in production?",
    ]),
    10: ("Retrieval & Matching Engine", [
        "How would you design a retrieval layer that can choose between SQL, vector search, and hybrid retrieval?",
        "What would you do when retrieval returns overlapping or low-quality results?",
    ]),
    12: ("Prompt Engineering Fundamentals", [
        "How would you design and evaluate a production system prompt for a technical chatbot?",
        "When would you use zero-shot versus few-shot prompting, and how would you measure which prompt is better?",
    ]),
    16: ("Chatbot Backend & API Integration", [
        "Walk me through the API flow from receiving a chatbot message to returning a grounded answer.",
        "How would you maintain conversation state across multiple API requests without losing important context?",
    ]),
    20: ("Conversation Memory & Context Management", [
        "What would you keep in conversation memory, and how would you manage token limits for a long interview?",
        "How would you summarize older messages while preserving facts that matter for later turns?",
    ]),
    21: ("LangChain Agents & Tool Use", [
        "What makes an agent different from a fixed function-calling workflow, and when would you choose an agent?",
        "How would you evaluate whether an agent is selecting the correct tool for a request?",
    ]),
    22: ("Multi-Agent Orchestration", [
        "When does a multi-agent architecture provide a real benefit over a single agent?",
        "How would you design a router that delegates a request to the correct specialist agent?",
    ]),
    23: ("Model Context Protocol (MCP)", [
        "What problem does MCP solve, and how does it standardize access to tools or capabilities?",
        "How would you secure and monitor an MCP server exposing tools to an AI agent?",
    ]),
    27: ("Security, Privacy & Guardrails", [
        "What are the main security risks for an AI application, and how would you defend against prompt injection?",
        "How would you validate untrusted input before it reaches tools or sensitive data sources?",
    ]),
    28: ("Docker & Kubernetes Deployment", [
        "What would you containerize in an AI application, and what configuration should never be hard-coded into the image?",
        "How would health checks and deployment configuration improve the reliability of an AI API?",
    ]),
    29: ("Monitoring, Logging & Observability", [
        "Which metrics would you monitor for a production AI API, and why?",
        "How would structured logs help you debug a slow or failing agent workflow?",
    ]),
    31: ("Capstone Project & Final Demo", [
        "Describe your capstone architecture and explain the most important engineering trade-off you made.",
        "If you had one more week to improve the capstone for production, what would you change and how would you measure it?",
    ]),
}

DEFAULT_DAYS = [7, 8, 10, 12]


def _completed_days(candidate: dict[str, Any]) -> list[int]:
    missions = candidate.get("missions")
    if not isinstance(missions, list):
        member = candidate.get("member")
        missions = member.get("missions", []) if isinstance(member, dict) else []
    result: list[int] = []
    for mission in missions:
        if not isinstance(mission, dict) or mission.get("passed") is not True:
            continue
        try:
            day = int(mission["day"])
        except (KeyError, TypeError, ValueError):
            continue
        if day in QUESTION_BANK and day not in result:
            result.append(day)
    return result


def _build_flow(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    days = _completed_days(candidate)
    for day in DEFAULT_DAYS:
        if day not in days:
            days.append(day)
        if len(days) == 4:
            break
    flow: list[dict[str, Any]] = []
    for day in days[:4]:
        title, questions = QUESTION_BANK[day]
        flow.extend({"day": day, "title": title, "question": q} for q in questions)
    return flow[:8]


def _feedback(messages: list[dict[str, Any]]) -> dict[str, Any]:
    answers = [str(item.get("answer", "")) for item in messages]
    combined = " ".join(answers).lower()
    detailed = sum(len(a.split()) >= 40 for a in answers)
    terms = ["embedding", "vector", "retrieval", "rag", "prompt", "agent", "mcp", "api", "docker", "security", "monitoring"]
    hits = sum(term in combined for term in terms)
    strengths: list[str] = []
    gaps: list[str] = []
    next_points = [
        "Use a clear structure: approach, reasoning/trade-off, implementation detail, and outcome.",
        "For production questions, mention reliability, security, observability, and cost when relevant.",
    ]
    if detailed >= 4:
        strengths.append("You gave detailed answers across the interview.")
    else:
        gaps.append("Add concrete examples, implementation details, and measurable outcomes.")
    if hits >= 5:
        strengths.append("You connected answers to relevant AI engineering concepts.")
    else:
        gaps.append("Use more precise technical terminology and explain why you chose an approach.")
    return {
        "summary": f"You completed {len(answers)} technical questions across multiple curriculum areas.",
        "strengths": strengths,
        "gaps": gaps,
        "next": next_points,
    }


def _parse(raw: str) -> list[dict[str, Any]]:
    try:
        value = json.loads(raw)
        return value if isinstance(value, list) else []
    except (TypeError, ValueError):
        return []


def _feedback_payload(interview: InterviewFlow) -> FeedbackPayload:
    return FeedbackPayload(
        summary=interview.feedback_summary or "",
        strengths=[x for x in (interview.feedback_strengths or "").split("||") if x],
        gaps=[x for x in (interview.feedback_gaps or "").split("||") if x],
        next=[x for x in (interview.feedback_next or "").split("||") if x],
    )


def _next_question(question: dict[str, Any], previous_answer: str) -> str:
    if len(previous_answer.split()) >= 15:
        return f"Building on what you said, let's go deeper into {question['title']}: {question['question']}"
    return f"Thanks. Let's go one level deeper into {question['title']}: {question['question']}"


@router.post("", response_model=InterviewResponse)
def handle_interview(payload: InterviewPayload, db: Session = Depends(get_db)) -> InterviewResponse:
    if payload.message is None:
        if payload.candidate is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="candidate is required for interview start.")
        if db.get(InterviewFlow, payload.sessionId) is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Interview session already exists.")

        flow = _build_flow(payload.candidate)
        interview = InterviewFlow(
            session_id=payload.sessionId,
            candidate_data=json.dumps({"candidate": payload.candidate, "flow": flow}, ensure_ascii=False),
            answers="[]",
            current_question=0,
            stage="active",
            status="active",
        )
        db.add(interview)
        db.commit()
        return InterviewResponse(reply="Welcome. Let's begin your interview.\n\n" + flow[0]["question"], done=False, feedback=None)

    interview = db.get(InterviewFlow, payload.sessionId)
    if interview is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found.")
    if interview.status != "active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Interview has already completed.")

    stored = json.loads(interview.candidate_data)
    flow = stored.get("flow", []) if isinstance(stored, dict) else []
    if len(flow) < 8:
        flow = _build_flow(stored.get("candidate", {}) if isinstance(stored, dict) else {})

    index = interview.current_question
    if index >= len(flow):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Interview question state is invalid.")

    answers = _parse(interview.answers)
    current = flow[index]
    answers.append({**current, "answer": payload.message})
    interview.answers = json.dumps(answers, ensure_ascii=False)
    interview.current_question += 1

    if interview.current_question >= len(flow):
        result = _feedback(answers)
        interview.status = "completed"
        interview.stage = "completed"
        interview.feedback_summary = result["summary"]
        interview.feedback_strengths = "||".join(result["strengths"])
        interview.feedback_gaps = "||".join(result["gaps"])
        interview.feedback_next = "||".join(result["next"])
        db.commit()
        return InterviewResponse(reply="Interview completed.", done=True, feedback=_feedback_payload(interview))

    db.commit()
    return InterviewResponse(reply=_next_question(flow[interview.current_question], payload.message), done=False, feedback=None)

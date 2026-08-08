"""AI service layer.

Wraps the OpenAI client to generate interview questions and evaluate
candidate answers. Every function falls back to deterministic, local
heuristics when no OPENAI_API_KEY is configured, so the app is fully
functional in development without external credentials.
"""
from __future__ import annotations

import json
import logging
from typing import Any

from openai import OpenAI

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_client: OpenAI | None = None


def _get_client() -> OpenAI | None:
    """Return a cached OpenAI client, or None if no API key is configured."""
    global _client
    if not settings.openai_api_key:
        return None
    if _client is None:
        _client = OpenAI(api_key=settings.openai_api_key, max_retries=0)
    return _client


def _json_extract(text: str) -> list[dict[str, Any]]:
    """Best-effort parse of a JSON array from an AI response."""
    text = text.strip()
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            logger.warning("Could not parse AI JSON payload; treating as single item.")
    return [{"content": text, "question_type": "custom", "difficulty": "medium"}]


# ---------------------------------------------------------------------------
# Question generation
# ---------------------------------------------------------------------------

_QUESTION_BANK: list[tuple[str, str, str]] = [
    ("Tell me about yourself and how your background aligns with this role.", "behavioral", "easy"),
    ("Describe a time you solved a difficult problem under pressure.", "behavioral", "medium"),
    ("Walk me through a project you're most proud of and your specific contribution.", "behavioral", "medium"),
    ("How do you handle disagreements with a teammate or stakeholder?", "situational", "medium"),
    ("What would you do if you inherited a legacy codebase with no tests?", "situational", "hard"),
    ("Explain a technical concept you know well as if teaching a junior engineer.", "technical", "medium"),
    ("What are your strengths, and where do you see room for growth?", "strengths", "easy"),
    ("Why are you interested in this role and our company?", "behavioral", "easy"),
]


def generate_questions_local(**kwargs: Any) -> list[dict[str, Any]]:
    """Return a deterministic bank of questions when no AI is configured."""
    count = int(kwargs.get("count") or 8)

    def _norm(t: Any) -> str:
        # Accept either enum members or plain strings.
        return t.value if hasattr(t, "value") else str(t)

    requested_types = {_norm(t) for t in kwargs.get("question_types") or []}
    questions: list[dict[str, Any]] = []
    for content, qtype, difficulty in _QUESTION_BANK:
        if requested_types and qtype not in requested_types:
            continue
        questions.append(
            {
                "content": content,
                "question_type": qtype,
                "difficulty": difficulty,
                "order": len(questions),
            }
        )
        if len(questions) >= count:
            break
    return questions


def generate_questions(
    job_title: str,
    job_description: str | None = None,
    candidate_skills: str | None = None,
    count: int = 8,
    question_types: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Generate interview questions via the AI, or fall back to local bank."""
    kwargs: dict[str, Any] = {
        "count": count,
        "question_types": question_types or ["behavioral", "technical", "situational"],
    }
    client = _get_client()
    if client is None:
        return generate_questions_local(**kwargs)

    type_list = ", ".join(question_types) if question_types else "behavioral, technical, situational"
    prompt = (
        f"You are an expert technical interviewer. Generate {count} interview questions "
        f"for the role of '{job_title}'.\n"
        f"Job description: {job_description or 'N/A'}\n"
        f"Candidate skills: {candidate_skills or 'N/A'}\n"
        f"Question types to include: {type_list}\n\n"
        "Return ONLY a JSON array of objects with keys: "
        '"content" (string), "question_type" (one of behavioral, technical, coding, '
        'situational, strengths, custom), "difficulty" (easy, medium, hard), "order" (int).'
    )
    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You generate interview questions as JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        content = response.choices[0].message.content or "[]"
        return _json_extract(content)[:count]
    except Exception as exc:  # noqa: BLE001 - never crash the API on AI errors
        logger.exception("AI question generation failed, using local bank: %s", exc)
        return generate_questions_local(**kwargs)



# ---------------------------------------------------------------------------
# Answer evaluation
# ---------------------------------------------------------------------------

def evaluate_answer_local(question: str, answer_text: str) -> dict[str, Any]:
    """Deterministic heuristic evaluation when no AI is configured.

    Scores based on answer length and keyword coverage, which is enough to
    exercise the full evaluation pipeline in development.
    """
    word_count = len(answer_text.split())
    base = min(10.0, max(1.0, word_count / 20.0))
    technical = min(10.0, base + 1.0) if any(
        kw in answer_text.lower() for kw in ("design", "architecture", "api", "sql", "code", "test", "scale", "system")
    ) else base
    communication = min(10.0, base + 1.0) if word_count >= 40 else max(1.0, base - 1.0)
    overall = round((technical + communication) / 2, 1)
    return {
        "score": overall,
        "communication_score": round(communication, 1),
        "technical_score": round(technical, 1),
        "feedback": "Your answer was reviewed. Add specific examples and walk through your reasoning for a stronger response.",
        "strengths": "Clear structure; relevant terminology." if word_count >= 30 else "Concise response.",
        "improvements": "Elaborate with concrete examples and quantify impact where possible.",
        "raw_ai_payload": None,
    }


def evaluate_answer(question: str, answer_text: str) -> dict[str, Any]:
    """Evaluate a candidate's answer via the AI, or fall back to heuristics."""
    client = _get_client()
    if client is None or not answer_text.strip():
        return evaluate_answer_local(question, answer_text)

    prompt = (
        "You are a fair, calibrated technical interviewer. Evaluate the following "
        "answer to the interview question and return ONLY JSON with keys: "
        '"score" (0-10 float), "communication_score" (0-10 float), '
        '"technical_score" (0-10 float), "feedback" (string), "strengths" (string), '
        '"improvements" (string).\n\n'
        f"Question: {question}\nAnswer: {answer_text}"
    )
    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You evaluate interview answers and return JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content or "{}"
        start, end = content.find("{"), content.rfind("}")
        if start != -1 and end != -1:
            payload = json.loads(content[start : end + 1])
            payload["raw_ai_payload"] = content
            return payload
    except Exception as exc:  # noqa: BLE001
        logger.exception("AI evaluation failed, using heuristics: %s", exc)
    return evaluate_answer_local(question, answer_text)


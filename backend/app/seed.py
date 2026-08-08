"""Seed the database with sample data for development/demo purposes.

Usage:  python -m app.seed
"""
from __future__ import annotations

import logging

from sqlalchemy import select

from app.database import SessionLocal, init_db
from app.models.candidate import Candidate
from app.models.session import InterviewSession
from app.services import ai

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def seed() -> None:
    init_db()
    with SessionLocal() as db:
        if db.scalar(select(Candidate)) is not None:
            logger.info("Database already seeded. Skipping.")
            return

        candidate = Candidate(
            full_name="Ada Lovelace",
            email="ada@example.com",
            phone="+1-555-0100",
            skills="Python, SQL, System Design, Algorithms",
            years_of_experience=5.0,
            resume_text="Senior software engineer with a focus on backend systems and data pipelines.",
        )
        db.add(candidate)
        db.flush()

        session = InterviewSession(
            candidate_id=candidate.id,
            job_title="Senior Backend Engineer",
            job_description="Own backend services, design scalable APIs, and mentor junior engineers.",
            status="scheduled",
        )
        db.add(session)
        db.flush()

        generated = ai.generate_questions(
            job_title=session.job_title,
            job_description=session.job_description,
            candidate_skills=candidate.skills,
            count=5,
        )
        for item in generated:
            from app.models.question import Question

            db.add(
                Question(
                    session_id=session.id,
                    content=item["content"],
                    question_type=item.get("question_type", "behavioral"),
                    difficulty=item.get("difficulty", "medium"),
                    order=item.get("order", 0),
                )
            )

        db.commit()
        logger.info("Seeded candidate id=%s and session id=%s", candidate.id, session.id)


if __name__ == "__main__":
    seed()

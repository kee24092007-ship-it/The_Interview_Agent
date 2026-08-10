import tempfile
import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


@pytest.fixture(scope="function")
def test_engine(tmp_path) -> Session:
    db_file = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(test_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(scope="function")
def client(monkeypatch, db_session: Session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr("app.services.ai.settings.openai_api_key", None)

    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_candidate_session_and_question_generation_flow(client: TestClient, db_session: Session):
    candidate_payload = {
        "full_name": "Test Candidate",
        "email": f"test+{uuid.uuid4().hex[:8]}@example.com",
        "phone": "555-0100",
        "resume_text": "Experienced developer.",
        "skills": "Python, FastAPI, SQL",
        "years_of_experience": 5,
    }

    response = client.post("/candidates", json=candidate_payload)
    assert response.status_code == 201
    candidate = response.json()
    assert candidate["email"] == candidate_payload["email"]

    session_payload = {
        "candidate_id": candidate["id"],
        "job_title": "Backend Engineer",
        "job_description": "Build APIs and services.",
        "status": "scheduled",
    }
    response = client.post("/sessions", json=session_payload)
    assert response.status_code == 201
    session = response.json()
    assert session["job_title"] == session_payload["job_title"]

    question_request = {
        "job_title": "Backend Engineer",
        "job_description": "Build APIs and services.",
        "candidate_skills": "Python, FastAPI, SQL",
        "count": 3,
        "question_types": ["behavioral", "technical"],
    }
    response = client.post(f"/sessions/{session['id']}/questions/generate", json=question_request)
    assert response.status_code == 201
    questions = response.json()
    assert len(questions) == 3
    assert all("content" in q for q in questions)

    response = client.get(f"/sessions/{session['id']}")
    assert response.status_code == 200
    session_details = response.json()
    assert session_details["candidate_id"] == candidate["id"]

    response = client.delete(f"/candidates/{candidate['id']}")
    assert response.status_code == 204

    response = client.get(f"/sessions/{session['id']}")
    assert response.status_code == 200
    session_after_delete = response.json()
    assert session_after_delete["id"] == session["id"]

    response = client.get(f"/candidates/{candidate['id']}")
    assert response.status_code == 404

"""Database engine, session factory and helpers (SQLAlchemy 2.x)."""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

settings = get_settings()

# SQLite requires check_same_thread=False when used with FastAPI threading.
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    # Set to True while developing to see every SQL statement.
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session and closes it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables defined in the models package."""
    # Importing the models module registers the tables on Base.metadata.
    from app.models import candidate, session as session_model, question, answer, evaluation  # noqa: F401

    Base.metadata.create_all(bind=engine)

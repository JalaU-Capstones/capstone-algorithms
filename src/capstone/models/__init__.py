"""Models package initialization and database setup."""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from capstone.config import get_cached_settings
from capstone.models.record import Base, StudentRecord, StudentRecordDTO

settings = get_cached_settings()

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def get_session() -> Generator[Session]:
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


__all__ = [
    "Base",
    "StudentRecord",
    "StudentRecordDTO",
    "engine",
    "SessionLocal",
    "get_session",
]

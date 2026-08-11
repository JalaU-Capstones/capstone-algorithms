"""Database models and Data Transfer Objects for the application."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for SQLAlchemy declarative models."""

    pass


class StudentRecord(Base):
    """Represents a student's performance record in the database."""

    __tablename__ = "student_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)


@dataclass
class StudentRecordDTO:
    """Data Transfer Object for StudentRecord."""

    id: int
    name: str
    category: str
    score: Decimal
    subject: str
    created_at: datetime

    @staticmethod
    def from_orm(record: StudentRecord) -> StudentRecordDTO:
        """Create a DTO from a SQLAlchemy model instance.

        Args:
            record: The SQLAlchemy model instance.

        Returns:
            StudentRecordDTO: The created DTO.
        """
        return StudentRecordDTO(
            id=record.id,
            name=record.name,
            category=record.category,
            score=record.score,
            subject=record.subject,
            created_at=record.created_at,
        )

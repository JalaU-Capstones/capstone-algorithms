"""Repository for managing StudentRecord entities."""

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from capstone.models.record import StudentRecord, StudentRecordDTO


class RecordRepository:
    """Repository class for abstracting database operations on StudentRecord."""

    def __init__(self, session: Session) -> None:
        """Initialize the repository with a database session.

        Args:
            session: SQLAlchemy session to execute queries.
        """
        self._session = session

    def create(
        self, name: str, category: str, score: Decimal, subject: str
    ) -> StudentRecordDTO:
        """Create a new StudentRecord in the database.

        Args:
            name: Student's name.
            category: Student's category (Junior, Mid, Senior, Expert).
            score: Student's score.
            subject: Evaluated subject.

        Returns:
            StudentRecordDTO: The created record as a DTO.
        """
        record = StudentRecord(
            name=name, category=category, score=score, subject=subject
        )
        self._session.add(record)
        self._session.commit()
        # Refresh to ensure id and created_at are loaded
        self._session.refresh(record)
        return StudentRecordDTO.from_orm(record)

    def get_all(self) -> list[StudentRecordDTO]:
        """Retrieve all student records, ordered by id ascending.

        Returns:
            list[StudentRecordDTO]: A list of all records.
        """
        stmt = select(StudentRecord).order_by(StudentRecord.id.asc())
        records = self._session.scalars(stmt).all()
        return [StudentRecordDTO.from_orm(r) for r in records]

    def get_by_id(self, record_id: int) -> StudentRecordDTO | None:
        """Retrieve a student record by its ID.

        Args:
            record_id: The ID of the record to retrieve.

        Returns:
            Optional[StudentRecordDTO]: The DTO if found, None otherwise.
        """
        record = self._session.get(StudentRecord, record_id)
        if record:
            return StudentRecordDTO.from_orm(record)
        return None

    def update_score(
        self, record_id: int, new_score: Decimal
    ) -> StudentRecordDTO | None:
        """Update the score of an existing student record.

        Args:
            record_id: The ID of the record to update.
            new_score: The new score to set.

        Returns:
            Optional[StudentRecordDTO]: The updated DTO if found, None otherwise.
        """
        record = self._session.get(StudentRecord, record_id)
        if record:
            record.score = new_score
            self._session.commit()
            self._session.refresh(record)
            return StudentRecordDTO.from_orm(record)
        return None

    def delete(self, record_id: int) -> bool:
        """Delete a student record by its ID.

        Args:
            record_id: The ID of the record to delete.

        Returns:
            bool: True if the record was deleted, False if it was not found.
        """
        record = self._session.get(StudentRecord, record_id)
        if record:
            self._session.delete(record)
            self._session.commit()
            return True
        return False

    def count(self) -> int:
        """Count the total number of student records.

        Returns:
            int: The total count of records.
        """
        stmt = select(func.count()).select_from(StudentRecord)
        count = self._session.scalar(stmt)
        return count or 0

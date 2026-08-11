from decimal import Decimal

from sqlalchemy.orm import Session

from capstone.repository.record_repository import RecordRepository


def test_create_record(db_session: Session) -> None:
    repo = RecordRepository(db_session)
    record = repo.create("John Doe", "Junior", Decimal("85.50"), "Math")

    assert record.id is not None
    assert record.name == "John Doe"
    assert record.category == "Junior"
    assert record.score == Decimal("85.50")
    assert record.subject == "Math"
    assert record.created_at is not None


def test_get_all_returns_list(db_session: Session) -> None:
    repo = RecordRepository(db_session)
    repo.create("Alice", "Junior", Decimal("80"), "Math")
    repo.create("Bob", "Mid", Decimal("90"), "Science")
    repo.create("Charlie", "Senior", Decimal("95"), "History")

    records = repo.get_all()
    assert len(records) == 3
    assert records[0].name == "Alice"
    assert records[1].name == "Bob"
    assert records[2].name == "Charlie"


def test_get_by_id_found(db_session: Session) -> None:
    repo = RecordRepository(db_session)
    created = repo.create("John Doe", "Junior", Decimal("85.50"), "Math")

    retrieved = repo.get_by_id(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.name == "John Doe"


def test_get_by_id_not_found(db_session: Session) -> None:
    repo = RecordRepository(db_session)
    retrieved = repo.get_by_id(999)
    assert retrieved is None


def test_update_score(db_session: Session) -> None:
    repo = RecordRepository(db_session)
    record = repo.create("John Doe", "Junior", Decimal("85.50"), "Math")

    updated = repo.update_score(record.id, Decimal("90.00"))
    assert updated is not None
    assert updated.score == Decimal("90.00")

    retrieved = repo.get_by_id(record.id)
    assert retrieved is not None
    assert retrieved.score == Decimal("90.00")


def test_delete_existing(db_session: Session) -> None:
    repo = RecordRepository(db_session)
    record = repo.create("John Doe", "Junior", Decimal("85.50"), "Math")

    assert repo.count() == 1
    deleted = repo.delete(record.id)
    assert deleted is True
    assert repo.count() == 0
    assert repo.get_by_id(record.id) is None


def test_delete_non_existing(db_session: Session) -> None:
    repo = RecordRepository(db_session)
    deleted = repo.delete(999)
    assert deleted is False


def test_update_non_existing(db_session: Session) -> None:
    repo = RecordRepository(db_session)
    updated = repo.update_score(999, Decimal("90.00"))
    assert updated is None


def test_count(db_session: Session) -> None:
    repo = RecordRepository(db_session)
    assert repo.count() == 0

    repo.create("Alice", "Junior", Decimal("80"), "Math")
    assert repo.count() == 1

    repo.create("Bob", "Mid", Decimal("90"), "Science")
    assert repo.count() == 2

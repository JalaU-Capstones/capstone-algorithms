"""Integration tests for RecordService wired to the real test database.
Exercises the full stack: service → repository → PostgreSQL.
Date: August 2026
"""

from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from capstone.repository.record_repository import RecordRepository
from capstone.services.record_service import RecordService


@pytest.fixture
def service(db_session: Session) -> RecordService:
    """Build a RecordService backed by the transactional test session."""
    repo = RecordRepository(db_session)
    return RecordService(repository=repo)


# ─────────────────────────────────────────
# CRUD
# ─────────────────────────────────────────


def test_create_and_retrieve_record(service: RecordService) -> None:
    """Creating a record and fetching it by ID returns all matching fields."""
    record = service.create_record(
        name="Integration Alice",
        category="Junior",
        score=Decimal("87.50"),
        subject="Mathematics",
    )

    assert record.id is not None
    retrieved = service.get_record_by_id(record.id)
    assert retrieved is not None
    assert retrieved.name == "Integration Alice"
    assert retrieved.category == "Junior"
    assert retrieved.score == Decimal("87.50")
    assert retrieved.subject == "Mathematics"
    assert retrieved.created_at is not None


def test_create_invalid_score_raises(service: RecordService) -> None:
    """Scores outside [0, 100] are rejected with a ValueError."""
    with pytest.raises(ValueError, match="Score must be between"):
        service.create_record(
            name="Bad Score",
            category="Mid",
            score=Decimal("150.00"),
            subject="Physics",
        )


def test_create_invalid_category_raises(service: RecordService) -> None:
    """Unknown category values are rejected with a ValueError."""
    with pytest.raises(ValueError, match="Invalid category"):
        service.create_record(
            name="Bad Category",
            category="Unknown",
            score=Decimal("75.00"),
            subject="History",
        )


def test_get_all_records_returns_created(service: RecordService) -> None:
    """All records created within the session are returned by get_all_records."""
    service.create_record("Alpha", "Junior", Decimal("70.00"), "Science")
    service.create_record("Beta", "Mid", Decimal("80.00"), "Math")
    service.create_record("Gamma", "Senior", Decimal("90.00"), "English")

    all_records = service.get_all_records()
    assert len(all_records) >= 3


def test_delete_record(service: RecordService) -> None:
    """Deleting a record makes it unretrievable via get_record_by_id."""
    record = service.create_record(
        name="To Delete",
        category="Expert",
        score=Decimal("55.00"),
        subject="Art",
    )
    record_id = record.id

    deleted = service.delete_record(record_id)
    assert deleted is True
    assert service.get_record_by_id(record_id) is None


# ─────────────────────────────────────────
# Search
# ─────────────────────────────────────────


def test_search_linear_by_category(service: RecordService) -> None:
    """Linear search by category returns only matching records."""
    service.create_record("Carlos", "Junior", Decimal("65.00"), "Math")
    service.create_record("Diana", "Senior", Decimal("92.00"), "Physics")
    service.create_record("Eli", "Junior", Decimal("78.00"), "History")

    result = service.search_records("category", "Junior", algorithm="linear")
    assert isinstance(result, list)
    assert len(result) >= 2
    for r in result:
        assert r.category == "Junior"


def test_search_binary_by_score(service: RecordService) -> None:
    """Binary search by score finds a record with the target value."""
    target_score = Decimal("83.00")
    service.create_record("Frank", "Mid", target_score, "Chemistry")
    service.create_record("Grace", "Senior", Decimal("91.00"), "Biology")

    result = service.search_records("score", target_score, algorithm="binary")
    # binary_search returns DTO or None — must find the target
    assert result is not None
    from capstone.models.record import StudentRecordDTO

    assert isinstance(result, StudentRecordDTO)
    assert result.score == target_score


# ─────────────────────────────────────────
# Sort
# ─────────────────────────────────────────


def test_sort_by_score_ascending(service: RecordService) -> None:
    """Bubble sort by score ascending produces a non-decreasing sequence."""
    service.create_record("Hank", "Junior", Decimal("55.00"), "Math")
    service.create_record("Iris", "Mid", Decimal("88.00"), "Science")
    service.create_record("Jake", "Senior", Decimal("72.00"), "History")

    sorted_records = service.sort_records("score", algorithm="bubble")
    for i in range(len(sorted_records) - 1):
        assert sorted_records[i].score <= sorted_records[i + 1].score


def test_sort_by_name_descending(service: RecordService) -> None:
    """Insertion sort by name descending produces a reverse-lexicographic sequence."""
    service.create_record("Zelda", "Expert", Decimal("99.00"), "CS")
    service.create_record("Aaron", "Junior", Decimal("61.00"), "Math")
    service.create_record("Monica", "Mid", Decimal("75.00"), "Physics")

    sorted_records = service.sort_records("name", reverse=True, algorithm="insertion")
    for i in range(len(sorted_records) - 1):
        assert sorted_records[i].name.lower() >= sorted_records[i + 1].name.lower()


# ─────────────────────────────────────────
# Statistics
# ─────────────────────────────────────────


def test_get_statistics_structure(service: RecordService) -> None:
    """Statistics summary contains all required keys with correct total count."""
    service.create_record("Stat1", "Junior", Decimal("60.00"), "Math")
    service.create_record("Stat2", "Mid", Decimal("75.00"), "Science")
    service.create_record("Stat3", "Senior", Decimal("85.00"), "History")
    service.create_record("Stat4", "Expert", Decimal("95.00"), "CS")

    stats = service.get_statistics()
    assert "total" in stats
    assert "max_score" in stats
    assert "min_score" in stats
    assert "average_score" in stats
    assert "by_category" in stats
    assert isinstance(stats["total"], int)
    assert stats["total"] >= 4

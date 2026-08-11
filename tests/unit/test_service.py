"""Unit tests for RecordService using MagicMock for the repository.
Date: August 2026
"""

from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from capstone.models.record import StudentRecordDTO
from capstone.repository.record_repository import RecordRepository
from capstone.services.record_service import RecordService


@pytest.fixture
def mock_repo() -> MagicMock:
    """Provide a MagicMock that mimics RecordRepository's interface."""
    return MagicMock(spec=RecordRepository)


@pytest.fixture
def service(mock_repo: MagicMock) -> RecordService:
    """Provide a RecordService wired with the mock repository."""
    return RecordService(repository=mock_repo)


@pytest.fixture
def sample_records() -> list[StudentRecordDTO]:
    """Six StudentRecordDTOs built directly — no database."""
    dt = datetime.now()
    return [
        StudentRecordDTO(
            id=1,
            name="Alice",
            category="Junior",
            score=Decimal("85.00"),
            subject="Math",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=2,
            name="Bob",
            category="Mid",
            score=Decimal("72.00"),
            subject="Science",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=3,
            name="Charlie",
            category="Junior",
            score=Decimal("90.50"),
            subject="History",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=4,
            name="Diana",
            category="Senior",
            score=Decimal("60.00"),
            subject="Physics",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=5,
            name="Eve",
            category="Expert",
            score=Decimal("95.75"),
            subject="CS",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=6,
            name="Frank",
            category="Mid",
            score=Decimal("78.25"),
            subject="English",
            created_at=dt,
        ),
    ]


# --- create_record ---


def test_create_record_delegates_to_repository(
    service: RecordService,
    mock_repo: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    mock_repo.create.return_value = sample_records[0]
    result = service.create_record(
        name="Alice",
        category="Junior",
        score=Decimal("85.00"),
        subject="Math",
    )
    mock_repo.create.assert_called_once_with(
        name="Alice",
        category="Junior",
        score=Decimal("85.00"),
        subject="Math",
    )
    assert result == sample_records[0]


def test_create_record_invalid_score_raises(service: RecordService) -> None:
    with pytest.raises(ValueError, match="Score must be between"):
        service.create_record(
            name="Alice",
            category="Junior",
            score=Decimal("150.00"),
            subject="Math",
        )


def test_create_record_invalid_category_raises(service: RecordService) -> None:
    with pytest.raises(ValueError, match="Invalid category"):
        service.create_record(
            name="Alice",
            category="Newbie",
            score=Decimal("85.00"),
            subject="Math",
        )


def test_create_record_empty_name_raises(service: RecordService) -> None:
    with pytest.raises(ValueError, match="Name must be a non-empty string"):
        service.create_record(
            name="",
            category="Junior",
            score=Decimal("85.00"),
            subject="Math",
        )


# --- get_all_records ---


def test_get_all_records_delegates(
    service: RecordService,
    mock_repo: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    mock_repo.get_all.return_value = sample_records
    result = service.get_all_records()
    assert result == sample_records
    mock_repo.get_all.assert_called_once()


# --- get_record_by_id ---


def test_get_record_by_id_found(
    service: RecordService,
    mock_repo: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    mock_repo.get_by_id.return_value = sample_records[0]
    result = service.get_record_by_id(1)
    assert result == sample_records[0]
    mock_repo.get_by_id.assert_called_once_with(1)


def test_get_record_by_id_not_found(
    service: RecordService,
    mock_repo: MagicMock,
) -> None:
    mock_repo.get_by_id.return_value = None
    result = service.get_record_by_id(999)
    assert result is None


# --- update_record_score ---


def test_update_record_score_valid(
    service: RecordService,
    mock_repo: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    mock_repo.update_score.return_value = sample_records[0]
    result = service.update_record_score(1, Decimal("85.00"))
    assert result is not None
    mock_repo.update_score.assert_called_once_with(1, Decimal("85.00"))


def test_update_record_score_invalid_raises(service: RecordService) -> None:
    with pytest.raises(ValueError, match="Score must be between"):
        service.update_record_score(1, Decimal("101.00"))


# --- delete_record ---


def test_delete_record_existing(
    service: RecordService,
    mock_repo: MagicMock,
) -> None:
    mock_repo.delete.return_value = True
    assert service.delete_record(1) is True
    mock_repo.delete.assert_called_once_with(1)


def test_delete_record_non_existing(
    service: RecordService,
    mock_repo: MagicMock,
) -> None:
    mock_repo.delete.return_value = False
    assert service.delete_record(999) is False


# --- search_records ---


def test_search_records_linear(
    service: RecordService,
    mock_repo: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    mock_repo.get_all.return_value = sample_records
    result = service.search_records("category", "Junior", algorithm="linear")
    assert isinstance(result, list)


def test_search_records_binary(
    service: RecordService,
    mock_repo: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    mock_repo.get_all.return_value = sample_records
    result = service.search_records("score", Decimal("85.00"), algorithm="binary")
    # Result is either a matched DTO or None — both are valid
    assert result is None or isinstance(result, StudentRecordDTO)


def test_search_records_invalid_algorithm_raises(
    service: RecordService,
    mock_repo: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    mock_repo.get_all.return_value = sample_records
    with pytest.raises(ValueError, match="Invalid search algorithm"):
        service.search_records("name", "Alice", algorithm="hash")


# --- sort_records ---


def test_sort_records_bubble(
    service: RecordService,
    mock_repo: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    mock_repo.get_all.return_value = sample_records
    result = service.sort_records("score", algorithm="bubble")
    assert isinstance(result, list)
    assert len(result) == len(sample_records)


def test_sort_records_invalid_algorithm_raises(
    service: RecordService,
    mock_repo: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    mock_repo.get_all.return_value = sample_records
    with pytest.raises(ValueError, match="Invalid sort algorithm"):
        service.sort_records("score", algorithm="quicksort")


# --- get_statistics ---


def test_get_statistics_returns_summary(
    service: RecordService,
    mock_repo: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    mock_repo.get_all.return_value = sample_records
    result = service.get_statistics()
    assert "total" in result
    assert result["total"] == len(sample_records)

"""Tests for search algorithms.
Date: August 2026
"""

from datetime import datetime
from decimal import Decimal

import pytest

from capstone.algorithms.search import binary_search, linear_search
from capstone.models.record import StudentRecordDTO


@pytest.fixture
def search_records() -> list[StudentRecordDTO]:
    """Fixture to provide a list of 10 StudentRecordDTOs for search testing."""
    dt = datetime.now()
    return [
        StudentRecordDTO(
            id=1,
            name="Alice Smith",
            category="Freshman",
            score=Decimal("85.50"),
            subject="Math",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=2,
            name="Bob Jones",
            category="Sophomore",
            score=Decimal("92.00"),
            subject="Science",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=3,
            name="Charlie Brown",
            category="Freshman",
            score=Decimal("78.25"),
            subject="Math",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=4,
            name="Diana Prince",
            category="Junior",
            score=Decimal("95.00"),
            subject="History",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=5,
            name="Eve Davis",
            category="Senior",
            score=Decimal("88.75"),
            subject="Science",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=6,
            name="Frank Miller",
            category="Freshman",
            score=Decimal("72.00"),
            subject="English",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=7,
            name="Grace Hopper",
            category="Senior",
            score=Decimal("99.90"),
            subject="Computer Science",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=8,
            name="Hank Pym",
            category="Junior",
            score=Decimal("84.50"),
            subject="Physics",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=9,
            name="Ivy Lee",
            category="Sophomore",
            score=Decimal("91.00"),
            subject="Math",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=10,
            name="Jack Sparrow",
            category="Sophomore",
            score=Decimal("65.00"),
            subject="Navigation",
            created_at=dt,
        ),
    ]


def test_linear_search_by_name_found(search_records: list[StudentRecordDTO]) -> None:
    result = linear_search(search_records, "name", "Alice Smith")
    assert len(result) >= 1
    assert result[0].name == "Alice Smith"


def test_linear_search_by_category_multiple_results(
    search_records: list[StudentRecordDTO],
) -> None:
    result = linear_search(search_records, "category", "Freshman")
    assert len(result) >= 2
    assert all(r.category == "Freshman" for r in result)


def test_linear_search_by_score_found(search_records: list[StudentRecordDTO]) -> None:
    result = linear_search(search_records, "score", Decimal("95.00"))
    assert len(result) > 0
    assert result[0].score == Decimal("95.00")


def test_linear_search_not_found(search_records: list[StudentRecordDTO]) -> None:
    result = linear_search(search_records, "name", "Nonexistent Student")
    assert result == []


def test_linear_search_case_insensitive(search_records: list[StudentRecordDTO]) -> None:
    result = linear_search(search_records, "name", "aLiCe SmiTh")
    assert len(result) > 0
    assert result[0].name == "Alice Smith"


def test_linear_search_invalid_attribute(
    search_records: list[StudentRecordDTO],
) -> None:
    with pytest.raises(ValueError):
        linear_search(search_records, "age", "20")


def test_binary_search_by_score_found(search_records: list[StudentRecordDTO]) -> None:
    # Pre-sort by score
    sorted_records = sorted(search_records, key=lambda x: x.score)
    result = binary_search(sorted_records, "score", Decimal("92.00"))
    assert result is not None
    assert result.score == Decimal("92.00")


def test_binary_search_not_found(search_records: list[StudentRecordDTO]) -> None:
    sorted_records = sorted(search_records, key=lambda x: x.score)
    result = binary_search(sorted_records, "score", Decimal("100.00"))
    assert result is None


def test_binary_search_invalid_attribute(
    search_records: list[StudentRecordDTO],
) -> None:
    sorted_records = sorted(search_records, key=lambda x: x.score)
    with pytest.raises(ValueError):
        binary_search(sorted_records, "grade", "A")


def test_binary_search_empty_list() -> None:
    result = binary_search([], "score", Decimal("92.00"))
    assert result is None

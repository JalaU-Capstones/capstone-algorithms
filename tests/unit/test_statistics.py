"""Unit tests for the statistics module.
Date: August 2026
"""

from datetime import datetime
from decimal import Decimal

import pytest

from capstone.models.record import StudentRecordDTO
from capstone.stats.statistics import (
    count_by_category,
    get_average_score,
    get_maximum_score,
    get_minimum_score,
    get_summary,
)


@pytest.fixture
def stats_records() -> list[StudentRecordDTO]:
    """Fixture: 10 StudentRecordDTOs with varied scores and 3+ categories."""
    dt = datetime.now()
    return [
        StudentRecordDTO(
            id=1,
            name="Alice",
            category="Junior",
            score=Decimal("55.00"),
            subject="Math",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=2,
            name="Bob",
            category="Mid",
            score=Decimal("72.50"),
            subject="Science",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=3,
            name="Charlie",
            category="Junior",
            score=Decimal("88.00"),
            subject="History",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=4,
            name="Diana",
            category="Senior",
            score=Decimal("91.75"),
            subject="Physics",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=5,
            name="Eve",
            category="Mid",
            score=Decimal("63.25"),
            subject="English",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=6,
            name="Frank",
            category="Expert",
            score=Decimal("99.00"),
            subject="CS",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=7,
            name="Grace",
            category="Junior",
            score=Decimal("42.50"),
            subject="Math",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=8,
            name="Hank",
            category="Senior",
            score=Decimal("77.80"),
            subject="Biology",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=9,
            name="Ivy",
            category="Expert",
            score=Decimal("95.00"),
            subject="CS",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=10,
            name="Jack",
            category="Mid",
            score=Decimal("60.20"),
            subject="Art",
            created_at=dt,
        ),
    ]


# --- get_maximum_score ---


def test_get_maximum_score_returns_highest(
    stats_records: list[StudentRecordDTO],
) -> None:
    result = get_maximum_score(stats_records)
    assert result == Decimal("99.00")


def test_get_maximum_score_empty_list() -> None:
    assert get_maximum_score([]) is None


# --- get_minimum_score ---


def test_get_minimum_score_returns_lowest(
    stats_records: list[StudentRecordDTO],
) -> None:
    result = get_minimum_score(stats_records)
    assert result == Decimal("42.50")


def test_get_minimum_score_empty_list() -> None:
    assert get_minimum_score([]) is None


# --- get_average_score ---


def test_get_average_score_correct_value(
    stats_records: list[StudentRecordDTO],
) -> None:
    scores = [
        Decimal("55.00"),
        Decimal("72.50"),
        Decimal("88.00"),
        Decimal("91.75"),
        Decimal("63.25"),
        Decimal("99.00"),
        Decimal("42.50"),
        Decimal("77.80"),
        Decimal("95.00"),
        Decimal("60.20"),
    ]
    expected = (sum(scores) / Decimal(len(scores))).quantize(Decimal("0.01"))
    result = get_average_score(stats_records)
    assert result == expected


def test_get_average_score_empty_list() -> None:
    assert get_average_score([]) is None


# --- count_by_category ---


def test_count_by_category_correct_counts(
    stats_records: list[StudentRecordDTO],
) -> None:
    result = count_by_category(stats_records)
    # Fixture has: Junior×3, Mid×3, Senior×2, Expert×2
    assert result["Junior"] == 3
    assert result["Mid"] == 3
    assert result["Senior"] == 2
    assert result["Expert"] == 2
    assert len(result) == 4


def test_count_by_category_empty_list() -> None:
    assert count_by_category([]) == {}


# --- get_summary ---


def test_get_summary_structure(stats_records: list[StudentRecordDTO]) -> None:
    result = get_summary(stats_records)
    assert "total" in result
    assert "max_score" in result
    assert "min_score" in result
    assert "average_score" in result
    assert "by_category" in result
    assert result["total"] == len(stats_records)


def test_get_summary_empty_list() -> None:
    result = get_summary([])
    assert result["total"] == 0
    assert result["max_score"] is None
    assert result["min_score"] is None
    assert result["average_score"] is None
    assert result["by_category"] == {}

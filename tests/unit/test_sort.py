"""Tests for sorting algorithms.
Date: August 2026
"""

from datetime import datetime
from decimal import Decimal

import pytest

from capstone.algorithms.sort import bubble_sort, insertion_sort, selection_sort
from capstone.models.record import StudentRecordDTO


@pytest.fixture
def sort_records() -> list[StudentRecordDTO]:
    """Fixture to provide a list of 8 StudentRecordDTOs for sort testing."""
    dt = datetime.now()
    return [
        StudentRecordDTO(
            id=1,
            name="Charlie",
            category="Freshman",
            score=Decimal("78.25"),
            subject="Math",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=2,
            name="Alice",
            category="Senior",
            score=Decimal("95.00"),
            subject="History",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=3,
            name="Eve",
            category="Sophomore",
            score=Decimal("88.75"),
            subject="Science",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=4,
            name="Bob",
            category="Junior",
            score=Decimal("84.50"),
            subject="Physics",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=5,
            name="Grace",
            category="Senior",
            score=Decimal("99.90"),
            subject="Computer Science",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=6,
            name="Frank",
            category="Freshman",
            score=Decimal("72.00"),
            subject="English",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=7,
            name="Diana",
            category="Junior",
            score=Decimal("92.00"),
            subject="Science",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=8,
            name="Hank",
            category="Sophomore",
            score=Decimal("91.00"),
            subject="Math",
            created_at=dt,
        ),
    ]


def test_bubble_sort_by_score_ascending(sort_records: list[StudentRecordDTO]) -> None:
    result = bubble_sort(sort_records, "score")
    for i in range(len(result) - 1):
        assert result[i].score <= result[i + 1].score


def test_bubble_sort_by_score_descending(sort_records: list[StudentRecordDTO]) -> None:
    result = bubble_sort(sort_records, "score", reverse=True)
    for i in range(len(result) - 1):
        assert result[i].score >= result[i + 1].score


def test_bubble_sort_by_name_ascending(sort_records: list[StudentRecordDTO]) -> None:
    result = bubble_sort(sort_records, "name")
    for i in range(len(result) - 1):
        assert result[i].name.lower() <= result[i + 1].name.lower()


def test_bubble_sort_does_not_mutate_input(
    sort_records: list[StudentRecordDTO],
) -> None:
    original_order = [r.id for r in sort_records]
    bubble_sort(sort_records, "score")
    assert [r.id for r in sort_records] == original_order


def test_bubble_sort_invalid_attribute(sort_records: list[StudentRecordDTO]) -> None:
    with pytest.raises(ValueError):
        bubble_sort(sort_records, "gpa")


def test_selection_sort_by_score_ascending(
    sort_records: list[StudentRecordDTO],
) -> None:
    result = selection_sort(sort_records, "score")
    for i in range(len(result) - 1):
        assert result[i].score <= result[i + 1].score


def test_selection_sort_by_category_ascending(
    sort_records: list[StudentRecordDTO],
) -> None:
    result = selection_sort(sort_records, "category")
    for i in range(len(result) - 1):
        assert result[i].category.lower() <= result[i + 1].category.lower()


def test_selection_sort_does_not_mutate_input(
    sort_records: list[StudentRecordDTO],
) -> None:
    original_order = [r.id for r in sort_records]
    selection_sort(sort_records, "score")
    assert [r.id for r in sort_records] == original_order


def test_insertion_sort_by_score_ascending(
    sort_records: list[StudentRecordDTO],
) -> None:
    result = insertion_sort(sort_records, "score")
    for i in range(len(result) - 1):
        assert result[i].score <= result[i + 1].score


def test_insertion_sort_by_subject_ascending(
    sort_records: list[StudentRecordDTO],
) -> None:
    result = insertion_sort(sort_records, "subject")
    for i in range(len(result) - 1):
        assert result[i].subject.lower() <= result[i + 1].subject.lower()


def test_insertion_sort_does_not_mutate_input(
    sort_records: list[StudentRecordDTO],
) -> None:
    original_order = [r.id for r in sort_records]
    insertion_sort(sort_records, "score")
    assert [r.id for r in sort_records] == original_order


def test_insertion_sort_already_sorted(sort_records: list[StudentRecordDTO]) -> None:
    sorted_records = sorted(sort_records, key=lambda r: r.score)
    result = insertion_sort(sorted_records, "score")
    for i in range(len(result) - 1):
        assert result[i].score <= result[i + 1].score


def test_all_sorts_produce_same_result(sort_records: list[StudentRecordDTO]) -> None:
    bubble_res = bubble_sort(sort_records, "score")
    selection_res = selection_sort(sort_records, "score")
    insertion_res = insertion_sort(sort_records, "score")

    assert [r.id for r in bubble_res] == [r.id for r in selection_res]
    assert [r.id for r in selection_res] == [r.id for r in insertion_res]


def test_sort_invalid_attribute(sort_records: list[StudentRecordDTO]) -> None:
    with pytest.raises(ValueError):
        selection_sort(sort_records, "rank")


def test_sort_empty_list() -> None:
    assert bubble_sort([], "score") == []
    assert selection_sort([], "score") == []
    assert insertion_sort([], "score") == []


def test_sort_single_element(sort_records: list[StudentRecordDTO]) -> None:
    single_list = [sort_records[0]]

    bubble_res = bubble_sort(single_list, "score")
    assert bubble_res == single_list
    assert bubble_res is not single_list

    selection_res = selection_sort(single_list, "score")
    assert selection_res == single_list
    assert selection_res is not single_list

    insertion_res = insertion_sort(single_list, "score")
    assert insertion_res == single_list
    assert insertion_res is not single_list

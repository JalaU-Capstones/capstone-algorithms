"""Sorting algorithms for StudentRecordDTO collections.
All functions operate on plain Python lists — no database access.
All sort functions return a NEW sorted list; the original is never mutated.
Date: August 2026
"""

from decimal import Decimal
from typing import Any

from capstone.models.record import StudentRecordDTO

VALID_SORT_ATTRIBUTES: frozenset[str] = frozenset(
    {"name", "category", "score", "subject"}
)


def _validate_sort_attribute(attribute: str) -> None:
    """Raise ValueError if attribute is not sortable."""
    if attribute not in VALID_SORT_ATTRIBUTES:
        raise ValueError(
            f"Invalid attribute: {attribute}. Must be one of {VALID_SORT_ATTRIBUTES}"
        )


def _get_attr_value(record: StudentRecordDTO, attribute: str) -> Any:
    """Return the attribute value from a record for comparison purposes.
    Converts str attributes to lowercase for case-insensitive ordering."""
    val = getattr(record, attribute)
    if isinstance(val, str):
        return val.lower()
    return val


def bubble_sort(
    records: list[StudentRecordDTO],
    attribute: str,
    reverse: bool = False,
) -> list[StudentRecordDTO]:
    """Perform a bubble sort on a list of StudentRecordDTOs.

    Args:
        records: List of StudentRecordDTO objects to sort.
        attribute: The attribute to sort by (name, category, score, subject).
        reverse: If True, sorts in descending order.

    Returns:
        A NEW sorted list of StudentRecordDTO objects.

    Raises:
        ValueError: If attribute is not valid.

    Best case O(n) with early exit, average and worst O(n²)
    """
    _validate_sort_attribute(attribute)
    result = records.copy()
    n = len(result)

    for i in range(n - 1):  # op: Outer loop iteration check
        swapped = False
        for j in range(n - 1 - i):  # op: Inner loop iteration check
            val1 = _get_attr_value(
                result[j], attribute
            )  # op: The attribute access for comparison (getattr x2)
            val2 = _get_attr_value(
                result[j + 1], attribute
            )  # op: The attribute access for comparison (getattr x2)

            # op: The comparison itself
            condition = val1 < val2 if reverse else val1 > val2

            if condition:
                temp = result[j]  # op: The swap (counts as 3 ops: temp, a=b, b=temp)
                result[j] = result[
                    j + 1
                ]  # op: The swap (counts as 3 ops: temp, a=b, b=temp)
                result[j + 1] = (
                    temp  # op: The swap (counts as 3 ops: temp, a=b, b=temp)
                )
                swapped = True

        if not swapped:  # op: The swapped flag check for early exit
            break

    return result


def selection_sort(
    records: list[StudentRecordDTO],
    attribute: str,
    reverse: bool = False,
) -> list[StudentRecordDTO]:
    """Perform a selection sort on a list of StudentRecordDTOs.

    Args:
        records: List of StudentRecordDTO objects to sort.
        attribute: The attribute to sort by (name, category, score, subject).
        reverse: If True, sorts in descending order.

    Returns:
        A NEW sorted list of StudentRecordDTO objects.

    Raises:
        ValueError: If attribute is not valid.

    O(n²) best, average and worst case
    """
    _validate_sort_attribute(attribute)
    result = records.copy()
    n = len(result)

    for i in range(n - 1):  # op: Outer loop iteration
        target_idx = i
        for j in range(i + 1, n):  # op: Inner loop iteration
            val_j = _get_attr_value(
                result[j], attribute
            )  # op: The attribute access for comparison (getattr x2)
            val_target = _get_attr_value(
                result[target_idx], attribute
            )  # op: The attribute access for comparison (getattr x2)

            # op: The comparison to update min_index
            condition = val_j > val_target if reverse else val_j < val_target
            if condition:
                target_idx = j

        if target_idx != i:
            temp = result[i]  # op: The conditional swap
            result[i] = result[target_idx]  # op: The conditional swap
            result[target_idx] = temp  # op: The conditional swap

    return result


def insertion_sort(
    records: list[StudentRecordDTO],
    attribute: str,
    reverse: bool = False,
) -> list[StudentRecordDTO]:
    """Perform an insertion sort on a list of StudentRecordDTOs.

    Args:
        records: List of StudentRecordDTO objects to sort.
        attribute: The attribute to sort by (name, category, score, subject).
        reverse: If True, sorts in descending order.

    Returns:
        A NEW sorted list of StudentRecordDTO objects.

    Raises:
        ValueError: If attribute is not valid.

    O(n) best case (already sorted), O(n²) average and worst
    """
    _validate_sort_attribute(attribute)
    result = records.copy()
    n = len(result)

    for i in range(1, n):  # op: Outer loop iteration
        key_record = result[i]
        key_val = _get_attr_value(key_record, attribute)  # op: Key extraction (getattr)

        j = i - 1

        # op: Inner while loop condition (comparison + index check)
        while j >= 0:
            compare_val = _get_attr_value(result[j], attribute)
            condition = compare_val < key_val if reverse else compare_val > key_val

            if not condition:
                break

            result[j + 1] = result[j]  # op: The shift operation (arr[j+1] = arr[j])
            j -= 1

        result[j + 1] = key_record  # op: The insertion (arr[j+1] = key_record)

    return result

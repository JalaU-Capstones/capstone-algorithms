"""Search algorithms for StudentRecordDTO collections.
All functions operate on plain Python lists — no database access.
Date: August 2026
"""

from decimal import Decimal
from typing import Any

from capstone.models.record import StudentRecordDTO

VALID_ATTRIBUTES: frozenset[str] = frozenset({"name", "category", "score", "subject"})


def _validate_attribute(attribute: str) -> None:
    """Raise ValueError if attribute is not searchable."""
    if attribute not in VALID_ATTRIBUTES:
        raise ValueError(
            f"Invalid attribute: {attribute}. Must be one of {VALID_ATTRIBUTES}"
        )


def linear_search(
    records: list[StudentRecordDTO],
    attribute: str,
    value: str | Decimal,
) -> list[StudentRecordDTO]:
    """Perform a linear search on a list of StudentRecordDTOs.

    Args:
        records: List of StudentRecordDTO objects to search.
        attribute: The attribute to search by (name, category, score, subject).
        value: The value to search for.

    Returns:
        A list of all matching StudentRecordDTOs.

    Raises:
        ValueError: If attribute is not one of: name, category, score, subject.

    Time complexity: O(n) worst and average case, O(1) best case
    Space complexity: O(k) where k is the number of matches
    """
    _validate_attribute(attribute)
    result = []

    n = len(records)
    i = 0
    while i < n:  # op: The loop iteration check (i < n)
        record = records[i]
        attr_val = getattr(record, attribute)  # op: The attribute access (getattr)

        # op: The comparison
        if isinstance(attr_val, str) and isinstance(value, str):
            match = attr_val.lower() == value.lower()
        else:
            match = attr_val == value

        if match:
            result.append(record)  # op: The conditional append

        i += 1

    return result


def binary_search(
    records: list[StudentRecordDTO],
    attribute: str,
    value: str | Decimal,
) -> StudentRecordDTO | None:
    """Perform an iterative binary search on a list of StudentRecordDTOs.

    Precondition:
        The `records` list must be sorted by the given `attribute` in ascending order.

    Args:
        records: List of StudentRecordDTO objects to search.
        attribute: The attribute to search by (name, category, score, subject).
        value: The value to search for.

    Returns:
        The first matching StudentRecordDTO found, or None if not found.

    Raises:
        ValueError: If attribute is not one of: name, category, score, subject.

    Time complexity: O(log n) worst and average, O(1) best
    Space complexity: O(1)
    """
    _validate_attribute(attribute)

    low = 0
    high = len(records) - 1

    while low <= high:  # op: The while loop condition check (low <= high)
        mid = (low + high) // 2  # op: The mid calculation
        record = records[mid]
        attr_val = getattr(record, attribute)  # op: The attribute access (getattr)

        # Prepare values for comparison
        comp_val: Any = attr_val.lower() if isinstance(attr_val, str) else attr_val
        target_val: Any = value.lower() if isinstance(value, str) else value

        if comp_val == target_val:  # op: The comparison to determine left/right
            return record
        elif comp_val < target_val:
            low = mid + 1  # op: The pointer update (low = mid + 1 or high = mid - 1)
        else:
            high = mid - 1  # op: The pointer update (low = mid + 1 or high = mid - 1)

    return None

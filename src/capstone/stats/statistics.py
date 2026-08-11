"""Statistics processing module for StudentRecordDTO collections.
All functions receive plain Python lists — no database access.
Results are returned as plain Python dicts or scalars.
Date: August 2026
"""

from decimal import Decimal

from capstone.models.record import StudentRecordDTO


def get_maximum_score(records: list[StudentRecordDTO]) -> Decimal | None:
    """Find the maximum score in a list of student records using a manual pass.

    Iterates through all records in a single pass, tracking the highest score
    seen so far. Does not use Python's built-in max() function.

    Args:
        records: A list of StudentRecordDTO objects to inspect.

    Returns:
        The maximum score as a Decimal, or None if the list is empty.

    Time complexity: O(n) — see docs/complexity/stats_analysis.md
    """
    if not records:
        return None

    max_score: Decimal = records[0].score  # op: initialize max to first element
    i = 1
    n = len(records)

    while i < n:  # op: loop condition check (i < n)
        current = records[i].score  # op: attribute access (getattr score)
        if current > max_score:  # op: comparison with current max
            max_score = current  # op: conditional update of max
        i += 1  # op: increment loop counter

    return max_score


def get_minimum_score(records: list[StudentRecordDTO]) -> Decimal | None:
    """Find the minimum score in a list of student records using a manual pass.

    Iterates through all records in a single pass, tracking the lowest score
    seen so far. Does not use Python's built-in min() function.

    Args:
        records: A list of StudentRecordDTO objects to inspect.

    Returns:
        The minimum score as a Decimal, or None if the list is empty.

    Time complexity: O(n) — see docs/complexity/stats_analysis.md
    """
    if not records:
        return None

    min_score: Decimal = records[0].score  # op: initialize min to first element
    i = 1
    n = len(records)

    while i < n:  # op: loop condition check (i < n)
        current = records[i].score  # op: attribute access (getattr score)
        if current < min_score:  # op: comparison with current min
            min_score = current  # op: conditional update of min
        i += 1  # op: increment loop counter

    return min_score


def get_average_score(records: list[StudentRecordDTO]) -> Decimal | None:
    """Calculate the average score across all student records.

    Accumulates a running sum in a single pass, then divides by the total
    count. Returns a Decimal rounded to 2 decimal places.

    Args:
        records: A list of StudentRecordDTO objects to process.

    Returns:
        The average score as a Decimal rounded to 2 decimal places,
        or None if the list is empty.

    Time complexity: O(n) — see docs/complexity/stats_analysis.md
    """
    if not records:
        return None

    total: Decimal = Decimal("0")  # op: initialize accumulator
    n = len(records)
    i = 0

    while i < n:  # op: loop condition check (i < n)
        total += records[i].score  # op: attribute access + accumulation
        i += 1  # op: increment loop counter

    average = total / Decimal(n)  # op: division to compute mean
    return average.quantize(Decimal("0.01"))


def count_by_category(records: list[StudentRecordDTO]) -> dict[str, int]:
    """Count how many records belong to each category.

    Performs a single pass through the list, building a frequency dictionary
    keyed by the exact category string found in each record.

    Args:
        records: A list of StudentRecordDTO objects to process.

    Returns:
        A dictionary mapping category names to their occurrence count.
        Returns an empty dict if the list is empty.

    Time complexity: O(n) — see docs/complexity/stats_analysis.md
    """
    counts: dict[str, int] = {}  # op: initialize frequency dict
    n = len(records)
    i = 0

    while i < n:  # op: loop condition check (i < n)
        category = records[i].category  # op: attribute access (getattr category)
        if category in counts:  # op: dict membership check
            counts[category] += 1  # op: increment existing count
        else:
            counts[category] = 1  # op: insert new category with count 1
        i += 1  # op: increment loop counter

    return counts


def get_summary(records: list[StudentRecordDTO]) -> dict[str, object]:
    """Produce a full statistical summary for a list of student records.

    Delegates computation to the four individual statistics functions and
    assembles the results into a single structured dictionary.

    Args:
        records: A list of StudentRecordDTO objects to summarise.

    Returns:
        A dictionary with the following keys:
            "total"         (int)              — total number of records
            "max_score"     (Decimal | None)   — highest score found
            "min_score"     (Decimal | None)   — lowest score found
            "average_score" (Decimal | None)   — mean score, 2 d.p.
            "by_category"   (dict[str, int])   — frequency per category

    Time complexity: O(n) — see docs/complexity/stats_analysis.md
    """
    return {
        "total": len(records),
        "max_score": get_maximum_score(records),
        "min_score": get_minimum_score(records),
        "average_score": get_average_score(records),
        "by_category": count_by_category(records),
    }

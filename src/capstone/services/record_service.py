"""Service layer for the Student Performance Analysis System.
Orchestrates RecordRepository, search/sort algorithms, and statistics functions.
This is the only layer that coordinates data access with business logic.
Date: August 2026
"""

from decimal import Decimal

from capstone.algorithms.search import binary_search, linear_search
from capstone.algorithms.sort import bubble_sort, insertion_sort, selection_sort
from capstone.models.record import StudentRecordDTO
from capstone.repository.record_repository import RecordRepository
from capstone.stats.statistics import get_summary

VALID_CATEGORIES: frozenset[str] = frozenset({"Junior", "Mid", "Senior", "Expert"})


class RecordService:
    """Orchestrates data access and algorithm execution.

    Depends on RecordRepository via constructor injection (Dependency Inversion).
    This class is the single point of coordination between the repository layer,
    the algorithm functions, and the statistics module.
    """

    def __init__(self, repository: RecordRepository) -> None:
        """Initialise the service with a repository instance.

        Args:
            repository: An instance of RecordRepository.
                        Injected to enable testing with mocks.
        """
        self._repository = repository

    def create_record(
        self,
        name: str,
        category: str,
        score: Decimal,
        subject: str,
    ) -> StudentRecordDTO:
        """Validate inputs and create a new student record.

        Args:
            name: Student's full name. Must be a non-empty string.
            category: Student category. Must be one of: Junior, Mid, Senior, Expert.
            score: Evaluation score. Must be in the range [0.00, 100.00].
            subject: Evaluated subject/course. Must be a non-empty string.

        Returns:
            The newly created StudentRecordDTO.

        Raises:
            ValueError: If name is empty.
            ValueError: If subject is empty.
            ValueError: If category is not one of the valid categories.
            ValueError: If score is outside the range [0.00, 100.00].
        """
        if not name or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        if not subject or not subject.strip():
            raise ValueError("Subject must be a non-empty string.")
        if category not in VALID_CATEGORIES:
            raise ValueError(
                f"Invalid category '{category}'. "
                f"Must be one of: {sorted(VALID_CATEGORIES)}."
            )
        if score < Decimal("0.00") or score > Decimal("100.00"):
            raise ValueError(
                f"Score must be between 0.00 and 100.00 (inclusive). Got {score}."
            )
        return self._repository.create(
            name=name.strip(),
            category=category,
            score=score,
            subject=subject.strip(),
        )

    def get_all_records(self) -> list[StudentRecordDTO]:
        """Retrieve all student records from the repository.

        Returns:
            A list of all StudentRecordDTOs ordered by ID ascending.
        """
        return self._repository.get_all()

    def get_record_by_id(self, record_id: int) -> StudentRecordDTO | None:
        """Retrieve a single student record by its primary key.

        Args:
            record_id: The integer ID of the record to retrieve.

        Returns:
            The matching StudentRecordDTO, or None if not found.
        """
        return self._repository.get_by_id(record_id)

    def update_record_score(
        self,
        record_id: int,
        new_score: Decimal,
    ) -> StudentRecordDTO | None:
        """Update the score of an existing student record.

        Args:
            record_id: The integer ID of the record to update.
            new_score: The new score value. Must be in [0.00, 100.00].

        Returns:
            The updated StudentRecordDTO, or None if the record was not found.

        Raises:
            ValueError: If new_score is outside the range [0.00, 100.00].
        """
        if new_score < Decimal("0.00") or new_score > Decimal("100.00"):
            raise ValueError(
                f"Score must be between 0.00 and 100.00 (inclusive). Got {new_score}."
            )
        return self._repository.update_score(record_id, new_score)

    def delete_record(self, record_id: int) -> bool:
        """Delete a student record by its primary key.

        Args:
            record_id: The integer ID of the record to delete.

        Returns:
            True if the record was found and deleted, False otherwise.
        """
        return self._repository.delete(record_id)

    def search_records(
        self,
        attribute: str,
        value: str | Decimal,
        algorithm: str = "linear",
    ) -> list[StudentRecordDTO] | StudentRecordDTO | None:
        """Search student records by attribute value using the specified algorithm.

        Fetches all records from the repository first, then delegates the
        search to the appropriate algorithm function.

        Note: When algorithm is "binary", the full record list is first sorted
        by the target attribute using insertion_sort (O(n) best case) before
        binary search is applied, because binary search requires sorted input.

        Args:
            attribute: The record field to search on.
                       Must be one of: name, category, score, subject.
            value: The value to search for.
            algorithm: Which search algorithm to use.
                       "linear" returns a list of all matches.
                       "binary" returns the first match or None.
                       Defaults to "linear".

        Returns:
            list[StudentRecordDTO] when algorithm is "linear".
            StudentRecordDTO | None when algorithm is "binary".

        Raises:
            ValueError: If algorithm is not "linear" or "binary".
            ValueError: If attribute is not a valid searchable field.
        """
        if algorithm not in {"linear", "binary"}:
            raise ValueError(
                f"Invalid search algorithm '{algorithm}'. Must be 'linear' or 'binary'."
            )
        records = self._repository.get_all()
        if algorithm == "linear":
            return linear_search(records, attribute, value)
        # binary: pre-sort by attribute, then search
        sorted_records = insertion_sort(records, attribute)
        return binary_search(sorted_records, attribute, value)

    def sort_records(
        self,
        attribute: str,
        reverse: bool = False,
        algorithm: str = "bubble",
    ) -> list[StudentRecordDTO]:
        """Sort all student records by a given attribute and algorithm.

        Fetches all records from the repository, then delegates sorting to
        the chosen algorithm function. Always returns a new list.

        Args:
            attribute: The record field to sort by.
                       Must be one of: name, category, score, subject.
            reverse: If True, sort in descending order. Defaults to False.
            algorithm: Which sort algorithm to use.
                       "bubble"    → bubble_sort
                       "selection" → selection_sort
                       "insertion" → insertion_sort
                       Defaults to "bubble".

        Returns:
            A new sorted list of StudentRecordDTOs.

        Raises:
            ValueError: If algorithm is not one of the supported values.
            ValueError: If attribute is not a valid sortable field.
        """
        sort_dispatch = {
            "bubble": bubble_sort,
            "selection": selection_sort,
            "insertion": insertion_sort,
        }
        if algorithm not in sort_dispatch:
            raise ValueError(
                f"Invalid sort algorithm '{algorithm}'. "
                f"Must be one of: {sorted(sort_dispatch)}."
            )
        records = self._repository.get_all()
        sort_fn = sort_dispatch[algorithm]
        return sort_fn(records, attribute, reverse)

    def get_statistics(self) -> dict[str, object]:
        """Compute and return a statistical summary of all student records.

        Fetches all records from the repository and delegates computation to
        the statistics module's get_summary function.

        Returns:
            A dict with keys: total, max_score, min_score,
            average_score, by_category.
        """
        records = self._repository.get_all()
        return get_summary(records)

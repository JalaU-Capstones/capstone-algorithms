"""Unit tests for MenuController and the main entry point.
Uses unittest.mock to intercept Console I/O — no real terminal interaction.
Date: August 2026
"""

from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from capstone.cli.menu import MenuController
from capstone.models.record import StudentRecordDTO
from capstone.services.record_service import RecordService

# ─────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────


@pytest.fixture
def mock_service() -> MagicMock:
    """MagicMock that mimics RecordService's interface."""
    return MagicMock(spec=RecordService)


@pytest.fixture
def controller(mock_service: MagicMock) -> MenuController:
    """MenuController wired with the mock service."""
    return MenuController(service=mock_service)


@pytest.fixture
def sample_record() -> StudentRecordDTO:
    """A single StudentRecordDTO for use in assertions."""
    return StudentRecordDTO(
        id=1,
        name="Alice",
        category="Junior",
        score=Decimal("85.00"),
        subject="Math",
        created_at=datetime(2026, 8, 11, 10, 0, 0),
    )


@pytest.fixture
def sample_records(sample_record: StudentRecordDTO) -> list[StudentRecordDTO]:
    """A small list of StudentRecordDTOs."""
    dt = datetime(2026, 8, 11, 10, 0, 0)
    return [
        sample_record,
        StudentRecordDTO(
            id=2,
            name="Bob",
            category="Senior",
            score=Decimal("92.00"),
            subject="Science",
            created_at=dt,
        ),
        StudentRecordDTO(
            id=3,
            name="Charlie",
            category="Junior",
            score=Decimal("70.00"),
            subject="History",
            created_at=dt,
        ),
    ]


# ─────────────────────────────────────────
# run() — menu dispatch
# ─────────────────────────────────────────


def test_run_exits_on_option_6(controller: MenuController) -> None:
    """Selecting option 6 causes run() to return without error."""
    with (
        patch.object(controller._console, "input", return_value="6"),
        patch.object(controller._console, "print"),
    ):
        controller.run()  # must return; not raise


def test_run_invalid_option_then_exit(controller: MenuController) -> None:
    """An invalid option shows an error message; subsequent valid selection exits."""
    inputs = iter(["9", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    # Verify that an error message was printed
    error_calls = [c for c in mock_print.call_args_list if "Invalid option" in str(c)]
    assert len(error_calls) >= 1


def test_run_handles_keyboard_interrupt(controller: MenuController) -> None:
    """KeyboardInterrupt during input results in a graceful goodbye message."""
    with (
        patch.object(controller._console, "input", side_effect=KeyboardInterrupt),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    goodbye_calls = [c for c in mock_print.call_args_list if "Interrupted" in str(c)]
    assert len(goodbye_calls) >= 1


# ─────────────────────────────────────────
# Option 1 — Register
# ─────────────────────────────────────────


def test_handle_register_success(
    controller: MenuController,
    mock_service: MagicMock,
    sample_record: StudentRecordDTO,
) -> None:
    """Valid inputs create a record via the service."""
    mock_service.create_record.return_value = sample_record
    # Simulate: option 1 → name → category → score → subject → option 6
    inputs = iter(["1", "Alice", "Junior", "85.00", "Math", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print"),
    ):
        controller.run()
    mock_service.create_record.assert_called_once()


def test_handle_register_invalid_category_loops(
    controller: MenuController,
    mock_service: MagicMock,
    sample_record: StudentRecordDTO,
) -> None:
    """Invalid category is re-prompted until a valid one is provided."""
    mock_service.create_record.return_value = sample_record
    # "Newbie" is invalid → re-prompt → "Junior" is valid
    inputs = iter(["1", "Alice", "Newbie", "Junior", "85.00", "Math", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    error_calls = [c for c in mock_print.call_args_list if "Invalid category" in str(c)]
    assert len(error_calls) >= 1


def test_handle_register_invalid_score_loops(
    controller: MenuController,
    mock_service: MagicMock,
    sample_record: StudentRecordDTO,
) -> None:
    """Non-numeric and out-of-range scores are re-prompted."""
    mock_service.create_record.return_value = sample_record
    # "abc" → NaN → "200" → out of range → "85.00" → valid
    inputs = iter(["1", "Alice", "Junior", "abc", "200", "85.00", "Math", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    error_calls = [
        c
        for c in mock_print.call_args_list
        if "not a valid number" in str(c) or "0.00 and 100.00" in str(c)
    ]
    assert len(error_calls) >= 1


def test_handle_register_service_value_error(
    controller: MenuController,
    mock_service: MagicMock,
) -> None:
    """A ValueError from the service is displayed as an error, not raised."""
    mock_service.create_record.side_effect = ValueError("Score out of range")
    inputs = iter(["1", "Alice", "Junior", "85.00", "Math", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    error_calls = [c for c in mock_print.call_args_list if "Error" in str(c)]
    assert len(error_calls) >= 1


# ─────────────────────────────────────────
# Option 2 — List
# ─────────────────────────────────────────


def test_handle_list_shows_table(
    controller: MenuController,
    mock_service: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    """Non-empty record list renders a table via the console."""
    mock_service.get_all_records.return_value = sample_records
    inputs = iter(["2", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    mock_service.get_all_records.assert_called()
    assert mock_print.call_count >= 1


def test_handle_list_empty(
    controller: MenuController,
    mock_service: MagicMock,
) -> None:
    """Empty record list prints the 'No records found' message."""
    mock_service.get_all_records.return_value = []
    inputs = iter(["2", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    no_records_calls = [
        c for c in mock_print.call_args_list if "No records found" in str(c)
    ]
    assert len(no_records_calls) >= 1


# ─────────────────────────────────────────
# Option 3 — Search
# ─────────────────────────────────────────


def test_handle_search_linear_found(
    controller: MenuController,
    mock_service: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    """Linear search delegates to service and displays results table."""
    mock_service.search_records.return_value = sample_records
    # option 3 → attribute 1 (name) → "Alice" → algorithm 1 (linear) → exit
    inputs = iter(["3", "1", "Alice", "1", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print"),
    ):
        controller.run()
    mock_service.search_records.assert_called_once_with("name", "Alice", "linear")


def test_handle_search_linear_no_results(
    controller: MenuController,
    mock_service: MagicMock,
) -> None:
    """Empty linear search result displays 'No matches found' message."""
    mock_service.search_records.return_value = []
    inputs = iter(["3", "1", "Nobody", "1", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    no_match_calls = [c for c in mock_print.call_args_list if "No matches" in str(c)]
    assert len(no_match_calls) >= 1


def test_handle_search_binary_found(
    controller: MenuController,
    mock_service: MagicMock,
    sample_record: StudentRecordDTO,
) -> None:
    """Binary search delegates to service and displays a record panel."""
    mock_service.search_records.return_value = sample_record
    # option 3 → attribute 3 (score) → "85.00" → algorithm 2 (binary) → exit
    inputs = iter(["3", "3", "85.00", "2", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print"),
    ):
        controller.run()
    mock_service.search_records.assert_called_once_with(
        "score", Decimal("85.00"), "binary"
    )


def test_handle_search_binary_not_found(
    controller: MenuController,
    mock_service: MagicMock,
) -> None:
    """Binary search returning None displays 'No match found' message."""
    mock_service.search_records.return_value = None
    inputs = iter(["3", "3", "99.99", "2", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    no_match_calls = [
        c for c in mock_print.call_args_list if "No match found" in str(c)
    ]
    assert len(no_match_calls) >= 1


def test_handle_search_invalid_attribute_loops(
    controller: MenuController,
    mock_service: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    """Invalid attribute selection re-prompts until a valid one is given."""
    mock_service.search_records.return_value = sample_records
    # "9" invalid → "1" valid → "Alice" → algorithm "1" → exit
    inputs = iter(["3", "9", "1", "Alice", "1", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    error_calls = [c for c in mock_print.call_args_list if "1, 2, 3, or 4" in str(c)]
    assert len(error_calls) >= 1


# ─────────────────────────────────────────
# Option 4 — Sort
# ─────────────────────────────────────────


def test_handle_sort_ascending(
    controller: MenuController,
    mock_service: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    """Sort ascending delegates to service with reverse=False."""
    mock_service.sort_records.return_value = sample_records
    # option 4 → attribute 3 (score) → direction 1 (asc) → algorithm 1 (bubble) → exit
    inputs = iter(["4", "3", "1", "1", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print"),
    ):
        controller.run()
    mock_service.sort_records.assert_called_once_with(
        "score", reverse=False, algorithm="bubble"
    )


def test_handle_sort_descending(
    controller: MenuController,
    mock_service: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    """Sort descending delegates to service with reverse=True."""
    mock_service.sort_records.return_value = sample_records
    # option 4 → attr 1 (name) → direction 2 (desc) → algorithm 3 (insertion) → exit
    inputs = iter(["4", "1", "2", "3", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print"),
    ):
        controller.run()
    mock_service.sort_records.assert_called_once_with(
        "name", reverse=True, algorithm="insertion"
    )


def test_handle_sort_invalid_algorithm_loops(
    controller: MenuController,
    mock_service: MagicMock,
    sample_records: list[StudentRecordDTO],
) -> None:
    """Invalid sort algorithm selection re-prompts until valid."""
    mock_service.sort_records.return_value = sample_records
    # "9" invalid → "1" valid
    inputs = iter(["4", "3", "1", "9", "1", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    error_calls = [c for c in mock_print.call_args_list if "1, 2, or 3" in str(c)]
    assert len(error_calls) >= 1


# ─────────────────────────────────────────
# Option 5 — Statistics
# ─────────────────────────────────────────


def test_handle_statistics_displays_panel(
    controller: MenuController,
    mock_service: MagicMock,
) -> None:
    """Statistics panel is rendered when records exist."""
    mock_service.get_statistics.return_value = {
        "total": 3,
        "max_score": Decimal("95.00"),
        "min_score": Decimal("60.00"),
        "average_score": Decimal("78.33"),
        "by_category": {"Junior": 2, "Senior": 1},
    }
    inputs = iter(["5", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    mock_service.get_statistics.assert_called()
    assert mock_print.call_count >= 1


def test_handle_statistics_empty(
    controller: MenuController,
    mock_service: MagicMock,
) -> None:
    """No records shows the 'No records available' message instead of a panel."""
    mock_service.get_statistics.return_value = {
        "total": 0,
        "max_score": None,
        "min_score": None,
        "average_score": None,
        "by_category": {},
    }
    inputs = iter(["5", "6"])
    with (
        patch.object(controller._console, "input", side_effect=inputs),
        patch.object(controller._console, "print") as mock_print,
    ):
        controller.run()
    empty_calls = [
        c for c in mock_print.call_args_list if "No records available" in str(c)
    ]
    assert len(empty_calls) >= 1


# ─────────────────────────────────────────
# main.py bootstrap
# ─────────────────────────────────────────


def test_main_calls_controller_run() -> None:
    """main() builds all layers and calls controller.run() exactly once."""
    mock_controller = MagicMock()
    mock_controller.run = MagicMock()
    with (
        patch("capstone.main.SessionLocal", return_value=MagicMock()),
        patch("capstone.main.RecordRepository", return_value=MagicMock()),
        patch("capstone.main.RecordService", return_value=MagicMock()),
        patch("capstone.main.MenuController", return_value=mock_controller),
    ):
        import capstone.main as main_module

        main_module.main()
    mock_controller.run.assert_called_once()


def test_main_exits_on_fatal_error() -> None:
    """An exception during bootstrap triggers sys.exit(1)."""
    with (
        patch("capstone.main.SessionLocal", side_effect=RuntimeError("DB down")),
        patch("capstone.main.Console"),
        pytest.raises(SystemExit) as exc_info,
    ):
        import capstone.main as main_module

        main_module.main()
    assert exc_info.value.code == 1

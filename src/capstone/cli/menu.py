"""Interactive console menu for the Student Performance Analysis System.
Uses the rich library for styled terminal output.
Depends only on RecordService — never imports repository or DB modules.
Date: August 2026
"""

from decimal import Decimal, InvalidOperation

import rich.box as box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from capstone.models.record import StudentRecordDTO
from capstone.services.record_service import RecordService

_VALID_CATEGORIES = ("Junior", "Mid", "Senior", "Expert")
_ATTRIBUTE_MAP = {"1": "name", "2": "category", "3": "score", "4": "subject"}
_SORT_ALGORITHM_MAP = {"1": "bubble", "2": "selection", "3": "insertion"}
_SEARCH_ALGORITHM_MAP = {"1": "linear", "2": "binary"}


class MenuController:
    """Interactive console menu controller for the Student Performance Analysis System.

    Renders a rich-styled terminal menu and dispatches user selections to the
    appropriate RecordService methods. Never imports repository or DB modules.
    """

    def __init__(self, service: RecordService) -> None:
        """Initialise the controller with a service instance.

        Args:
            service: The RecordService that provides all business logic.
        """
        self._service = service
        self._console = Console()

    # ─────────────────────────────────────────
    # Main loop
    # ─────────────────────────────────────────

    def run(self) -> None:
        """Start the main menu loop.

        Displays the menu and dispatches to option handlers until the user
        selects Exit (6). Handles KeyboardInterrupt gracefully.
        """
        try:
            while True:
                self._display_menu()
                choice = self._console.input(
                    "[bold yellow]Select an option [1-6]: [/bold yellow]"
                ).strip()

                if choice == "1":
                    self._handle_register()
                elif choice == "2":
                    self._handle_list()
                elif choice == "3":
                    self._handle_search()
                elif choice == "4":
                    self._handle_sort()
                elif choice == "5":
                    self._handle_statistics()
                elif choice == "6":
                    self._handle_exit()
                    return
                else:
                    self._console.print(
                        f"[bold red]Invalid option '{choice}'. "
                        "Please enter a number between 1 and 6.[/bold red]"
                    )
        except KeyboardInterrupt:
            self._console.print("\n[bold yellow]Interrupted. Goodbye![/bold yellow]")

    # ─────────────────────────────────────────
    # Menu display
    # ─────────────────────────────────────────

    def _display_menu(self) -> None:
        """Render the main menu panel."""
        menu_text = (
            "\n"
            "  [bold cyan][1][/bold cyan] Register new record\n"
            "  [bold cyan][2][/bold cyan] List all records\n"
            "  [bold cyan][3][/bold cyan] Search records\n"
            "  [bold cyan][4][/bold cyan] Sort records\n"
            "  [bold cyan][5][/bold cyan] Show statistics\n"
            "  [bold cyan][6][/bold cyan] Exit\n"
        )
        panel = Panel(
            menu_text,
            title="[bold]Student Performance Analysis System[/bold]",
            subtitle="[dim]Algorithms 1 — Jala University | August 2026[/dim]",
            border_style="bold cyan",
            padding=(0, 2),
        )
        self._console.print(panel)

    # ─────────────────────────────────────────
    # Option 1 — Register new record
    # ─────────────────────────────────────────

    def _handle_register(self) -> None:
        """Prompt for all fields, validate, and create a new student record."""
        self._console.print("\n[bold cyan]── Register New Record ──[/bold cyan]")

        name = self._console.input("  Name: ").strip()

        # Category loop
        valid_str = " / ".join(_VALID_CATEGORIES)
        category = ""
        while True:
            category = self._console.input(
                f"  Category ([italic]{valid_str}[/italic]): "
            ).strip()
            if category in _VALID_CATEGORIES:
                break
            self._console.print(
                f"  [red]Invalid category '{category}'. "
                f"Must be one of: {valid_str}[/red]"
            )

        # Score loop
        score = Decimal("0")
        while True:
            raw = self._console.input("  Score (0.00 – 100.00): ").strip()
            try:
                score = Decimal(raw)
                if Decimal("0") <= score <= Decimal("100"):
                    break
                self._console.print(
                    "  [red]Score must be between 0.00 and 100.00.[/red]"
                )
            except InvalidOperation:
                self._console.print(f"  [red]'{raw}' is not a valid number.[/red]")

        subject = self._console.input("  Subject: ").strip()

        try:
            record = self._service.create_record(
                name=name,
                category=category,
                score=score,
                subject=subject,
            )
            self._render_record_panel(record, title="✅ Record Created Successfully")
        except ValueError as exc:
            self._console.print(f"[bold red]Error:[/bold red] {exc}")

    # ─────────────────────────────────────────
    # Option 2 — List all records
    # ─────────────────────────────────────────

    def _handle_list(self) -> None:
        """Fetch and display all student records in a rich Table."""
        self._console.print("\n[bold cyan]── All Records ──[/bold cyan]")
        records = self._service.get_all_records()
        if not records:
            self._console.print("[yellow]No records found.[/yellow]")
            return
        self._render_records_table(records, title="All Student Records")
        self._console.print(f"[dim]Total: {len(records)} record(s)[/dim]")

    # ─────────────────────────────────────────
    # Option 3 — Search records
    # ─────────────────────────────────────────

    def _handle_search(self) -> None:
        """Guide the user through attribute, value, and algorithm selection."""
        self._console.print("\n[bold cyan]── Search Records ──[/bold cyan]")

        attribute = self._prompt_attribute(label="Search")

        # Value input
        search_value: str | Decimal
        if attribute == "score":
            while True:
                raw = self._console.input("  Score to search: ").strip()
                try:
                    search_value = Decimal(raw)
                    break
                except InvalidOperation:
                    self._console.print(f"  [red]'{raw}' is not a valid number.[/red]")
        else:
            attr_label = attribute.capitalize()
            search_value = self._console.input(f"  {attr_label} to search: ").strip()

        algorithm = self._prompt_algorithm_search()

        try:
            result = self._service.search_records(attribute, search_value, algorithm)

            if algorithm == "linear":
                assert isinstance(result, list)
                if not result:
                    self._console.print("[yellow]No matches found.[/yellow]")
                else:
                    self._render_records_table(
                        result,
                        title=f"Linear Search Results — {len(result)} match(es)",
                    )
            else:
                # binary — result is DTO or None
                if result is None:
                    self._console.print("[yellow]No match found.[/yellow]")
                else:
                    assert isinstance(result, StudentRecordDTO)
                    self._render_record_panel(
                        result, title="Binary Search — Match Found"
                    )
        except ValueError as exc:
            self._console.print(f"[bold red]Error:[/bold red] {exc}")

    # ─────────────────────────────────────────
    # Option 4 — Sort records
    # ─────────────────────────────────────────

    def _handle_sort(self) -> None:
        """Guide the user through attribute, direction, and algorithm selection."""
        self._console.print("\n[bold cyan]── Sort Records ──[/bold cyan]")

        attribute = self._prompt_attribute(label="Sort")

        # Direction
        reverse = False
        while True:
            dir_choice = self._console.input(
                "  Direction — [1] Ascending  [2] Descending: "
            ).strip()
            if dir_choice == "1":
                break
            elif dir_choice == "2":
                reverse = True
                break
            self._console.print("  [red]Enter 1 or 2.[/red]")

        algorithm = self._prompt_algorithm_sort()
        direction_label = "descending" if reverse else "ascending"
        algo_label = algorithm.capitalize()

        try:
            records = self._service.sort_records(
                attribute, reverse=reverse, algorithm=algorithm
            )
            self._console.print(
                f"\n[dim]Sorted by [bold]{attribute}[/bold] "
                f"({direction_label}) using [bold]{algo_label} sort[/bold][/dim]"
            )
            if not records:
                self._console.print("[yellow]No records to display.[/yellow]")
            else:
                self._render_records_table(
                    records,
                    title=(
                        f"Sorted by {attribute} ({direction_label}) — {algo_label} Sort"
                    ),
                )
        except ValueError as exc:
            self._console.print(f"[bold red]Error:[/bold red] {exc}")

    # ─────────────────────────────────────────
    # Option 5 — Show statistics
    # ─────────────────────────────────────────

    def _handle_statistics(self) -> None:
        """Fetch and display summary statistics in a rich Panel."""
        stats = self._service.get_statistics()
        total = stats.get("total", 0)

        if not total:
            self._console.print("[yellow]No records available for statistics.[/yellow]")
            return

        by_category: dict[str, int] = {}
        raw_by_cat = stats.get("by_category")
        if isinstance(raw_by_cat, dict):
            by_category = raw_by_cat

        cat_lines = "\n".join(
            f"    [bold]{cat}[/bold]    : [cyan]{count}[/cyan]"
            for cat, count in sorted(by_category.items())
        )

        content = (
            f"  [bold]Total records[/bold]   : [cyan]{total}[/cyan]\n"
            f"  [bold]Maximum score[/bold]   : [cyan]{stats.get('max_score')}[/cyan]\n"
            f"  [bold]Minimum score[/bold]   : [cyan]{stats.get('min_score')}[/cyan]\n"
            "  [bold]Average score[/bold]   :"
            f" [cyan]{stats.get('average_score')}[/cyan]\n"
            "\n"
            "  [bold]Records by category:[/bold]\n"
            f"{cat_lines}"
        )

        self._console.print(
            Panel(
                content,
                title="[bold magenta]System Statistics[/bold magenta]",
                border_style="magenta",
                padding=(1, 2),
            )
        )

    # ─────────────────────────────────────────
    # Option 6 — Exit
    # ─────────────────────────────────────────

    def _handle_exit(self) -> None:
        """Display a farewell message and exit."""
        self._console.print(
            Panel(
                "  Thank you for using the Student Performance Analysis System.\n"
                "  [bold]Goodbye![/bold]",
                border_style="bold green",
                padding=(1, 2),
            )
        )

    # ─────────────────────────────────────────
    # Private helpers
    # ─────────────────────────────────────────

    def _render_records_table(
        self,
        records: list[StudentRecordDTO],
        title: str = "Records",
    ) -> None:
        """Render a formatted rich Table for a list of StudentRecordDTO objects.

        Args:
            records: The records to display.
            title: Caption shown above the table.
        """
        table = Table(
            title=title,
            box=box.ROUNDED,
            header_style="bold magenta",
            show_lines=False,
        )
        table.add_column("ID", style="dim", justify="right")
        table.add_column("Name", style="bold")
        table.add_column("Category", style="cyan")
        table.add_column("Score", justify="right", style="green")
        table.add_column("Subject")
        table.add_column("Created At", style="dim")

        for r in records:
            table.add_row(
                str(r.id),
                r.name,
                r.category,
                str(r.score),
                r.subject,
                r.created_at.strftime("%Y-%m-%d %H:%M"),
            )

        self._console.print(table)

    def _render_record_panel(
        self,
        record: StudentRecordDTO,
        title: str = "Record Found",
    ) -> None:
        """Render a formatted rich Panel for a single StudentRecordDTO.

        Args:
            record: The record to display.
            title: Panel title.
        """
        content = (
            f"  [bold]ID[/bold]         : [cyan]{record.id}[/cyan]\n"
            f"  [bold]Name[/bold]       : [cyan]{record.name}[/cyan]\n"
            f"  [bold]Category[/bold]   : [cyan]{record.category}[/cyan]\n"
            f"  [bold]Score[/bold]      : [cyan]{record.score}[/cyan]\n"
            f"  [bold]Subject[/bold]    : [cyan]{record.subject}[/cyan]\n"
            "  [bold]Created At[/bold] : [cyan]"
            f"{record.created_at.strftime('%Y-%m-%d %H:%M')}[/cyan]"
        )
        self._console.print(
            Panel(
                content,
                title=f"[bold green]{title}[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )

    def _prompt_attribute(self, label: str = "Search") -> str:
        """Prompt the user to select a record attribute and return its field name.

        Args:
            label: Contextual label shown in the prompt (e.g. "Search", "Sort").

        Returns:
            One of: "name", "category", "score", "subject".
        """
        self._console.print(
            f"\n  {label} by:\n"
            "    [cyan][1][/cyan] Name\n"
            "    [cyan][2][/cyan] Category\n"
            "    [cyan][3][/cyan] Score\n"
            "    [cyan][4][/cyan] Subject"
        )
        while True:
            choice = self._console.input("  Select attribute [1-4]: ").strip()
            if choice in _ATTRIBUTE_MAP:
                return _ATTRIBUTE_MAP[choice]
            self._console.print("  [red]Enter 1, 2, 3, or 4.[/red]")

    def _prompt_algorithm_search(self) -> str:
        """Prompt the user to select a search algorithm.

        Returns:
            "linear" or "binary".
        """
        self._console.print(
            "\n  Algorithm:\n"
            "    [cyan][1][/cyan] Linear search (finds all matches)\n"
            "    [cyan][2][/cyan] Binary search"
            " (finds one match, requires sorted input)"
        )
        while True:
            choice = self._console.input("  Select algorithm [1-2]: ").strip()
            if choice in _SEARCH_ALGORITHM_MAP:
                return _SEARCH_ALGORITHM_MAP[choice]
            self._console.print("  [red]Enter 1 or 2.[/red]")

    def _prompt_algorithm_sort(self) -> str:
        """Prompt the user to select a sort algorithm.

        Returns:
            "bubble", "selection", or "insertion".
        """
        self._console.print(
            "\n  Algorithm:\n"
            "    [cyan][1][/cyan] Bubble sort\n"
            "    [cyan][2][/cyan] Selection sort\n"
            "    [cyan][3][/cyan] Insertion sort"
        )
        while True:
            choice = self._console.input("  Select algorithm [1-3]: ").strip()
            if choice in _SORT_ALGORITHM_MAP:
                return _SORT_ALGORITHM_MAP[choice]
            self._console.print("  [red]Enter 1, 2, or 3.[/red]")

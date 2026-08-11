"""Database seeding script."""

import sys
from decimal import Decimal

from rich.console import Console

from capstone.models import get_session
from capstone.repository.record_repository import RecordRepository

console = Console()

SEED_DATA = [
    ("Alice Smith", "Junior", Decimal("85.50"), "Algorithms 1"),
    ("Bob Jones", "Mid", Decimal("92.00"), "Data Structures"),
    ("Charlie Brown", "Senior", Decimal("78.25"), "Operating Systems"),
    ("Diana Prince", "Expert", Decimal("99.99"), "Machine Learning"),
    ("Eve Davis", "Junior", Decimal("65.00"), "Algorithms 1"),
    ("Frank White", "Mid", Decimal("88.00"), "Data Structures"),
    ("Grace Hopper", "Expert", Decimal("100.00"), "Machine Learning"),
    ("Harry Potter", "Senior", Decimal("81.50"), "Operating Systems"),
    ("Ivy Taylor", "Junior", Decimal("74.00"), "Algorithms 1"),
    ("Jack Sparrow", "Mid", Decimal("60.00"), "Data Structures"),
    ("Karen Hill", "Senior", Decimal("89.50"), "Operating Systems"),
    ("Liam Neeson", "Expert", Decimal("95.00"), "Machine Learning"),
    ("Mia Wallace", "Junior", Decimal("90.00"), "Algorithms 1"),
    ("Noah Carter", "Mid", Decimal("77.75"), "Data Structures"),
    ("Olivia Pope", "Senior", Decimal("84.00"), "Operating Systems"),
]


def main() -> None:
    """Run the seed process."""
    console.print("[bold cyan]Starting database seed...[/bold cyan]")

    with get_session() as session:
        repo = RecordRepository(session)

        if repo.count() > 0:
            msg = "[yellow]Database already contains records. Skipping seed.[/yellow]"
            console.print(msg)
            sys.exit(0)

        for name, category, score, subject in SEED_DATA:
            record = repo.create(name, category, score, subject)
            console.print(
                f"[green]Inserted: {record.name} - {record.category} - "
                f"{record.score} - {record.subject}[/green]"
            )

        console.print(
            f"[bold green]Seeded {len(SEED_DATA)} records successfully.[/bold green]"
        )


if __name__ == "__main__":
    main()

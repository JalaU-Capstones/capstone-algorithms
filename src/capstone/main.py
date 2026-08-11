"""Application entry point for the Student Performance Analysis System.
Bootstraps all layers: database session → repository → service → CLI.
Date: August 2026
"""

import contextlib
import sys

from rich.console import Console

from capstone.cli.menu import MenuController
from capstone.models import SessionLocal
from capstone.repository.record_repository import RecordRepository
from capstone.services.record_service import RecordService


def main() -> None:
    """Bootstrap the full application stack and launch the interactive menu."""
    console = Console()
    session = None
    try:
        session = SessionLocal()
        repository = RecordRepository(session)
        service = RecordService(repository=repository)
        controller = MenuController(service=service)
        controller.run()
    except Exception as e:
        console.print(f"[bold red]Fatal error:[/bold red] {e}")
        sys.exit(1)
    finally:
        # Ensure the session is always closed on exit to prevent connection leaks
        if session is not None:
            with contextlib.suppress(Exception):
                session.close()


if __name__ == "__main__":
    main()

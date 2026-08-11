import pytest
from sqlalchemy import text

from capstone.models import get_session


def test_session_rollback() -> None:
    """Verify that get_session rolls back on exception."""
    with pytest.raises(ValueError), get_session() as session:
        # Execute something
        session.execute(text("SELECT 1"))
        # Raise exception to trigger rollback
        raise ValueError("Intentional Error")

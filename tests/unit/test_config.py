import pytest

from capstone.config import get_settings


def test_config_missing_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(
        RuntimeError, match="DATABASE_URL environment variable is not set"
    ):
        get_settings()

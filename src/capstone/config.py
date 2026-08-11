"""Configuration module for the Capstone Algorithms project."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


@dataclass
class Settings:
    """Settings for the application, loaded from environment variables."""

    DATABASE_URL: str


def get_settings() -> Settings:
    """Get the application settings.

    Returns:
        Settings: The current configuration settings.

    Raises:
        RuntimeError: If DATABASE_URL is not set in the environment.
    """
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is not set")
    return Settings(DATABASE_URL=database_url)


# Cache the settings instance
_settings: Settings | None = None


def get_cached_settings() -> Settings:
    """Get a cached instance of the settings."""
    global _settings
    if _settings is None:
        _settings = get_settings()
    return _settings

"""Application settings using Pydantic BaseSettings.

This module defines the Settings class which loads configuration values
from environment variables or a .env file.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings.

    Attributes:
        host (str): The host address for the application.
        port (int): The port number for the application.
    """

    host: str
    port: int

    class Config:
        """Pydantic configuration for environment variable loading."""
        env_file: str = ".env"

settings = Settings()

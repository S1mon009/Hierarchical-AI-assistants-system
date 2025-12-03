"""Application settings using Pydantic BaseSettings.

This module defines the `Settings` class which loads configuration
values from environment variables or a `.env` file.

It is used to manage environment-specific configuration such as
database connection details, API keys, or other system parameters.
The settings are automatically loaded when the application starts.

Example:
    ```python
    from src.config.config import settings

    print(settings.host)
    print(settings.port)
    ```
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    """Application configuration settings.

    This class defines the configuration model for the FastAPI application.
    It automatically reads environment variables from the system or from
    a `.env` file if one exists.

    Attributes:
        host (str): The host address where the FastAPI app should run.
        port (int): The port number used by the FastAPI app.
        bcrypt_salt_rounds (int): The number of salt rounds used by bcrypt for
            password hashing. Higher values increase security but also
            computational cost.

    Example:
        ```python
        settings = Settings()
        print(settings.bcrypt_salt_rounds)
        ```
    """

    host: str
    port: int
    bcrypt_salt_rounds: int
    supabase_url: str
    supabase_key: str
    supabase_anon_key: str
    supabase_service_role_key: str
    frontend_url: str

    model_config = SettingsConfigDict(env_file=".env")

config = Config()
"""Settings: Global application configuration instance.

This object is created at import time and provides access to
environment variables throughout the application.
"""

"""
This module exposes the project settings.

It imports the `settings` object from the internal settings module
and makes it available for external use. This allows centralized
access to configuration values across the project.

Module Attributes:
    settings (Settings): The application settings object containing
        all configurable parameters.
"""

from .settings import settings

__all__ = ["settings"]

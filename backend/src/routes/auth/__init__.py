"""Authentication routes package initializer.

This module exposes the `register_router`, which defines the user registration
endpoint for the FastAPI application. It allows the authentication routes to be
imported conveniently from the `src.routes.auth` package.

Example:
    ```python
    from src.routes.auth import register_router
    app.include_router(register_router)
    ```

Attributes:
    register_router (APIRouter): Router handling user registration endpoints.
"""
from src.routes.auth.register import router as register_router

__all__ = ["register_router"]

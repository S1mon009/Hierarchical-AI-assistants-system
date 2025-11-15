"""
Authentication routes package initializer.

This module exposes authentication routers for the FastAPI application.
It allows the routes to be imported conveniently from the `src.routes.auth`
package.

Routers:
    sign_up_router (APIRouter): Router handling user registration endpoints.
    sign_in_router (APIRouter): Router handling user login endpoints.

Example:
    ```python
    from src.routes.auth import sign_up_router, sign_in_router
    app.include_router(sign_up_router)
    app.include_router(sign_in_router)
    ```
"""

from .sign_up import router as sign_up_router
from .sign_in import router as sign_in_router

__all__ = ["sign_up_router", "sign_in_router"]

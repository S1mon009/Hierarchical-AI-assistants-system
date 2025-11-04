"""Authentication schemas package initializer.

This module exposes the `RegisterForm` Pydantic model, which is responsible
for validating user registration data such as username, email, and password.

It allows convenient imports from the `src.schemas.auth` package and keeps
authentication-related schemas organized within the project structure.

Example:
    ```python
    from src.schemas.auth import RegisterForm

    form = RegisterForm(
        username="user123",
        email="user@example.com",
        password="StrongPass1!",
        repeat_password="StrongPass1!"
    )
    ```

Attributes:
    RegisterForm (BaseModel): Pydantic model for validating registration input data.
"""

from src.schemas.auth.register import RegisterForm

__all__ = ["RegisterForm"]

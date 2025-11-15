"""
Authentication schemas package initializer.

This module exposes Pydantic models used for user authentication,
allowing convenient imports from the `src.schemas.auth` package.
It helps keep authentication-related schemas organized within the
project structure.

Schemas:
    SignUpModel (BaseModel): Pydantic model for validating user registration input,
        including username, email, password, and password confirmation.
    SignInModel (BaseModel): Pydantic model for validating user login input,
        including email and password.

Example:
    ```python
    from src.schemas.auth import SignUpModel, SignInModel

    signup_form = SignUpModel(
        username="user123",
        email="user@example.com",
        password="StrongPass1!",
        repeat_password="StrongPass1!"
    )

    signin_form = SignInModel(
        email="user@example.com",
        password="StrongPass1!"
    )
    ```
"""
from .sign_up import SignUpModel
from .sign_in import SignInModel

__all__ = ["SignUpModel", "SignInModel"]

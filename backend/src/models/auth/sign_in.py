"""
Sign-in schemas module.

This module defines Pydantic models used for user authentication (sign-in).
It provides validation for user credentials, including email format and
password complexity requirements.

Classes:
    SignInModel (BaseModel): Pydantic model representing a sign-in form,
        validating the email and password fields with custom complexity rules.

Example:
    ```python
    from src.schemas.auth.sign_in import SignInModel

    form = SignInModel(
        email="user@example.com",
        password="StrongPass1!"
    )
    ```
"""
import re
from pydantic import BaseModel, EmailStr, Field, field_validator

class SignInModel(BaseModel):
    """Pydantic model representing a sign-in form.

    Validates email and password fields.
    Includes custom validators for password strength.
    """

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        """Validate that the password meets complexity requirements.

        Checks for at least one uppercase letter, one lowercase letter,
        one digit, and one special character.

        Args:
            password (str): The password to validate.

        Raises:
            ValueError: If the password does not meet complexity requirements.

        Returns:
            str: The validated password.
        """
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character")
        return password

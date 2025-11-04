"""User registration schema using Pydantic BaseModel.

This module defines the RegisterForm class, which handles validation of user registration data.
It ensures that input fields such as username, email, and password meet specific format
and complexity requirements, including password confirmation.
"""
import re
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationInfo

class RegisterForm(BaseModel):
    """Pydantic model representing a registration form.

    Validates username, email, password, and repeat_password fields.
    Includes custom validators for password strength and password match.
    """

    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)
    repeat_password: str = Field(..., min_length=8, max_length=32)

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

    @field_validator("repeat_password")
    @classmethod
    def passwords_match(cls, repeat_password: str, info: ValidationInfo) -> str:
        """Validate that repeat_password matches password.

        Args:
            repeat_password (str): The repeated password to validate.
            info (ValidationInfo): Validator context containing other field values.

        Raises:
            ValueError: If repeat_password does not match password.

        Returns:
            str: The validated repeat_password.
        """
        password: str | None = info.data.get("password")
        if password and repeat_password != password:
            raise ValueError("Passwords do not match")
        return repeat_password

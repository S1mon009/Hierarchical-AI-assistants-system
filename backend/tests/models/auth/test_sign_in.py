"""
Tests for authentication Pydantic models.

This module contains unit tests for the authentication schemas defined
in `src.schemas.auth`, specifically `SignInModel`. The tests verify
correct model instantiation with valid data, as well as proper
validation errors for invalid email formats and weak passwords.

Test Functions:
    test_valid_auth_models(): Ensures valid SignInModel instances are created correctly.
    test_invalid_passwords(password: str): Ensures weak passwords raise ValidationError.
    test_email_format(email: str): Ensures invalid email formats raise ValidationError.

Example:
    ```bash
    pytest tests/schemas/test_sign_in.py
    ```
"""
import pytest
from pydantic import ValidationError
from src.models.auth import SignInModel

def test_valid_auth_models() -> None:
    """Verify that valid SignInModel instances are created correctly."""
    data = {
        "email": "test@example.com",
        "password": "StrongPass1!"
    }
    form = SignInModel(**data)
    assert form.email == "test@example.com"
    assert form.password == "StrongPass1!"

@pytest.mark.parametrize("password", [
    "weakpass",
    "WEAKPASS",
    "Weakpass",
    "Weakpass1",
    "We",
    "W" * 40 + "a1!"
])
def test_invalid_passwords(password: str) -> None:
    """Verify that SignInModel rejects weak passwords and raises ValidationError."""
    data = {
        "email": "user@example.com",
        "password": password
    }
    with pytest.raises(ValidationError):
        SignInModel(**data)

@pytest.mark.parametrize("email", [
    "plainaddress",
    "@missingusername.com",
    "username@.com",
    "username@com.",
    "username@com"
])
def test_email_format(email: str) -> None:
    """Verify that invalid email formats raise ValidationError in SignInModel."""
    data = {
        "email": email,
        "password": "StrongPass1!"
    }
    with pytest.raises(ValidationError):
        SignInModel(**data)

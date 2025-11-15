"""
Tests for the SignUpModel authentication schema.

This module contains unit tests for the `SignUpModel` defined in
`src.schemas.auth`. The tests verify correct model instantiation
with valid data and ensure proper validation errors are raised for
invalid input, including weak passwords, mismatched passwords,
invalid email formats, and usernames outside allowed length limits.

Test Functions:
    test_valid_auth_models(): Ensures valid SignUpModel instances are created correctly.
    test_invalid_passwords(password: str): Ensures weak passwords raise ValidationError.
    test_passwords_do_not_match(): Ensures mismatched passwords raise ValidationError.
    test_username_length(username: str): Ensures invalid username lengths raise ValidationError.
    test_email_format(email: str): Ensures invalid email formats raise ValidationError.

Example:
    ```bash
    pytest tests/schemas/test_sign_up.py
    ```
"""
import pytest
from pydantic import ValidationError
from src.models.auth import SignUpModel

def test_valid_auth_models() -> None:
    """Verify that valid SignUpModel instances are created correctly."""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "StrongPass1!",
        "repeat_password": "StrongPass1!"
    }
    form = SignUpModel(**data)
    assert form.username == "testuser"
    assert form.email == "test@example.com"
    assert form.password == "StrongPass1!"
    assert form.repeat_password == "StrongPass1!"

@pytest.mark.parametrize("password", [
    "weakpass",
    "WEAKPASS",
    "Weakpass",
    "Weakpass1",
    "We",
    "W" * 40 + "a1!"
])
def test_invalid_passwords(password: str) -> None:
    """Verify that SignUpModel rejects weak passwords and raises ValidationError."""
    data = {
        "username": "user",
        "email": "user@example.com",
        "password": password,
        "repeat_password": password,
    }
    with pytest.raises(ValidationError):
        SignUpModel(**data)

def test_passwords_do_not_match() -> None:
    """Verify that SignUpModel raises ValidationError when passwords do not match."""
    data = {
        "username": "user",
        "email": "user@example.com",
        "password": "StrongPass1!",
        "repeat_password": "StrongPass2!",
    }
    with pytest.raises(ValidationError) as exc_info:
        SignUpModel(**data)
    assert "Passwords do not match" in str(exc_info.value)

@pytest.mark.parametrize("username", [
    "ab",
    "a" * 33
])
def test_username_length(username: str) -> None:
    """Verify that SignUpModel rejects usernames outside allowed length limits."""
    data = {
        "username": username,
        "email": "a@b.com",
        "password": "StrongPass1!",
        "repeat_password": "StrongPass1!",
    }
    with pytest.raises(ValidationError):
        SignUpModel(**data)

@pytest.mark.parametrize("email", [
    "plainaddress",
    "@missingusername.com",
    "username@.com",
    "username@com.",
    "username@com"
])
def test_email_format(email: str) -> None:
    """Verify that invalid email formats raise ValidationError in SignUpModel."""
    data = {
        "username": "validuser",
        "email": email,
        "password": "StrongPass1!",
        "repeat_password": "StrongPass1!",
    }
    with pytest.raises(ValidationError):
        SignUpModel(**data)

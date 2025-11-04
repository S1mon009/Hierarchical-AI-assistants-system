"""Unit tests for the RegisterForm Pydantic model.

This module contains a suite of unit tests verifying the validation logic
of the RegisterForm model. It ensures that valid data passes validation,
while invalid inputs such as weak passwords, mismatched passwords, invalid
emails, or usernames outside the allowed length trigger appropriate
ValidationError exceptions.
"""
import pytest
from pydantic import ValidationError
from src.schemas.auth import RegisterForm


def test_valid_register_form() -> None:
    """Test that a valid registration form passes validation."""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "StrongPass1!",
        "repeat_password": "StrongPass1!"
    }
    form = RegisterForm(**data)
    assert form.username == "testuser"
    assert form.email == "test@example.com"


@pytest.mark.parametrize("password", [
    "weakpass",
    "WEAKPASS",
    "Weakpass",
    "Weakpass1",
    "We",
    "W" * 40 + "a1!"
])
def test_invalid_passwords(password: str) -> None:
    """Test that invalid passwords raise a ValidationError."""
    data = {
        "username": "user",
        "email": "user@example.com",
        "password": password,
        "repeat_password": password,
    }
    with pytest.raises(ValidationError):
        RegisterForm(**data)


def test_passwords_do_not_match() -> None:
    """Test that mismatched passwords raise a ValidationError."""
    data = {
        "username": "user",
        "email": "user@example.com",
        "password": "StrongPass1!",
        "repeat_password": "StrongPass2!",
    }
    with pytest.raises(ValidationError) as exc_info:
        RegisterForm(**data)
    assert "Passwords do not match" in str(exc_info.value)


@pytest.mark.parametrize("username", [
    "ab",
    "a" * 33
])
def test_username_length(username: str) -> None:
    """Test that usernames outside the allowed length raise a ValidationError."""
    data = {
        "username": username,
        "email": "a@b.com",
        "password": "StrongPass1!",
        "repeat_password": "StrongPass1!",
    }
    with pytest.raises(ValidationError):
        RegisterForm(**data)


@pytest.mark.parametrize("email", [
    "plainaddress",
    "@missingusername.com",
    "username@.com",
    "username@com.",
    "username@com"
])
def test_email_format(email: str) -> None:
    """Test that invalid email formats raise a ValidationError."""
    data = {
        "username": "validuser",
        "email": email,
        "password": "StrongPass1!",
        "repeat_password": "StrongPass1!",
    }
    with pytest.raises(ValidationError):
        RegisterForm(**data)

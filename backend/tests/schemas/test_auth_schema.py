"""
Unit tests for authentication Pydantic schemas.

This module contains pytest-based unit tests for the `SignInSchema` and `SignUpSchema`
defined in `src.modules.auth.auth_schema`. The tests cover:

- Creation of valid schema instances
- Validation of password strength rules
- Validation of email format
- Matching of passwords in SignUpSchema
- Username length constraints
"""
import pytest
from pydantic import ValidationError
from src.modules.auth.auth_schema import SignInSchema, SignUpSchema, SignInResponseSchema

def test_valid_auth_models() -> None:
    """
    Test creation of valid SignInSchema and SignUpSchema instances.

    Ensures that valid input data produces schema instances with
    the expected attribute values.
    """
    sign_in_schema_data = {
        "email": "test@example.com",
        "password": "StrongPass1!"
    }
    sign_in_schema = SignInSchema(**sign_in_schema_data)
    assert sign_in_schema.email == "test@example.com"
    assert sign_in_schema.password == "StrongPass1!"

    sign_up_schema_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "StrongPass1!",
        "repeat_password": "StrongPass1!"
    }
    sign_up_schema = SignUpSchema(**sign_up_schema_data)
    assert sign_up_schema.username == "testuser"
    assert sign_up_schema.email == "test@example.com"
    assert sign_up_schema.password == "StrongPass1!"
    assert sign_up_schema.repeat_password == "StrongPass1!"


@pytest.mark.parametrize("password", [
    "weakpass",
    "WEAKPASS",
    "Weakpass",
    "Weakpass1",
    "We",
    "W" * 40 + "a1!"
])
def test_invalid_passwords(password: str) -> None:
    """
    Test that weak passwords are rejected by both schemas.

    Args:
        password (str): Passwords that do not meet the required strength criteria.

    Raises:
        ValidationError: If the schema allows weak passwords, the test fails.
    """
    sign_in_data = {
        "email": "user@example.com",
        "password": password
    }
    with pytest.raises(ValidationError):
        SignInSchema(**sign_in_data)

    sign_up_data = {
        "username": "user",
        "email": "user@example.com",
        "password": password,
        "repeat_password": password,
    }
    with pytest.raises(ValidationError):
        SignUpSchema(**sign_up_data)


@pytest.mark.parametrize("email", [
    "plainaddress",
    "@missingusername.com",
    "username@.com",
    "username@com.",
    "username@com"
])
def test_email_format(email: str) -> None:
    """
    Test that invalid email formats raise ValidationError.

    Args:
        email (str): Email strings with invalid formats.

    Raises:
        ValidationError: If the schema allows invalid email formats, the test fails.
    """
    sign_in_data = {
        "email": email,
        "password": "StrongPass1!"
    }
    with pytest.raises(ValidationError):
        SignInSchema(**sign_in_data)

    sign_up_data = {
        "username": "validuser",
        "email": email,
        "password": "StrongPass1!",
        "repeat_password": "StrongPass1!",
    }
    with pytest.raises(ValidationError):
        SignUpSchema(**sign_up_data)


def test_passwords_do_not_match() -> None:
    """
    Test that SignUpSchema rejects mismatched passwords.

    Raises:
        ValidationError: If `password` and `repeat_password` differ, a ValidationError is raised.
    """
    data = {
        "username": "user",
        "email": "user@example.com",
        "password": "StrongPass1!",
        "repeat_password": "StrongPass2!",
    }
    with pytest.raises(ValidationError) as exc_info:
        SignUpSchema(**data)
    assert "Passwords do not match" in str(exc_info.value)


@pytest.mark.parametrize("username", [
    "ab",
    "a" * 33
])
def test_username_length(username: str) -> None:
    """
    Test that SignUpSchema enforces username length constraints.

    Args:
        username (str): Usernames that are too short or too long.

    Raises:
        ValidationError: If the schema allows usernames outside the allowed length, the test fails.
    """
    sign_up_data = {
        "username": username,
        "email": "a@b.com",
        "password": "StrongPass1!",
        "repeat_password": "StrongPass1!",
    }
    with pytest.raises(ValidationError):
        SignUpSchema(**sign_up_data)

def test_sign_in_response_schema_valid() -> None:
    """
    Test creation of a valid SignInResponseSchema instance.

    Ensures that valid input data produces a schema instance with
    correctly nested UserOutSchema and SessionOutSchema objects.
    """
    data = {
        "message": "Login successful",
        "user": {"id": "1", "email": "test@example.com", "username": "tester"},
        "session": {"access_token": "abc", "refresh_token": "def"}
    }
    response = SignInResponseSchema(**data)
    assert response.user.email == "test@example.com"
    assert response.session.access_token == "abc"

def test_sign_in_response_schema_invalid() -> None:
    """
    Test that SignInResponseSchema rejects invalid nested data.

    Raises:
        ValidationError: If nested schemas have invalid fields or missing keys.
    """
    data = {
        "message": "Login successful",
        "user": {"id": 1, "email": "not-an-email", "username": "tester"},
        "session": {"access_token": "abc"}
    }
    with pytest.raises(ValidationError):
        SignInResponseSchema(**data)

import pytest
from pydantic import ValidationError
from src.schemas.auth import RegisterForm

def test_valid_register_form():
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
def test_invalid_passwords(password):
    data = {
        "username": "user",
        "email": "user@example.com",
        "password": password,
        "repeat_password": password,
    }
    with pytest.raises(ValidationError):
        RegisterForm(**data)


def test_passwords_do_not_match():
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
def test_username_length(username):
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
def test_email_format(email):
    data = {
        "username": "validuser",
        "email": email,
        "password": "StrongPass1!",
        "repeat_password": "StrongPass1!",
    }
    with pytest.raises(ValidationError):
        RegisterForm(**data)
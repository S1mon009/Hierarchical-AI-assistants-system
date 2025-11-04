"""Test suite for the authentication routes.

This module contains unit tests for the `/register` endpoint defined in
`src.routes.auth`. It ensures that the registration process correctly handles
valid and invalid input data, and that password hashing works as expected.

The tests use FastAPI's `TestClient` for integration-style testing
of the API routes.

Modules:
    - test_register_success: Tests successful registration with valid data.
    - test_register_passwords_do_not_match: Tests response when passwords mismatch.
    - test_register_missing_field: Tests validation when a required field is missing.
"""
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.routes.auth import register_router as router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_register_success(monkeypatch: any) -> None:
    """Test successful user registration.

    This test verifies that the `/register` endpoint correctly hashes the password
    using bcrypt and returns a successful HTTP 200 response when valid form data
    is submitted.

    The bcrypt salt rounds are temporarily reduced using `monkeypatch` to speed
    up test execution.

    Args:
        monkeypatch: pytest fixture used to dynamically modify the application
                     configuration (bcrypt salt rounds).

    Asserts:
        - Response status code is 200.
        - Response JSON contains a "message" key.
        - The hashed password begins with `$2`, indicating a bcrypt hash.
    """
    monkeypatch.setattr("src.config.config.settings.bcrypt_salt_rounds", 4)

    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test1234!",
            "repeat_password": "Test1234!"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"].startswith("$2"), "Hash bcrypt powinien zaczynać się od '$2'"


def test_register_passwords_do_not_match() -> None:
    """Test registration failure when passwords do not match.

    This test ensures that the endpoint correctly returns an HTTP 400 error
    when the provided `password` and `repeat_password` fields differ.

    Asserts:
        - Response status code is 400.
        - The response contains a `detail` field with information about the error.
        - The error message mentions `repeat_password`.
    """
    response = client.post(
        "/register",
        data={
            "username": "user",
            "email": "user@example.com",
            "password": "Test1234!",
            "repeat_password": "WrongPass123"
        }
    )

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert any("repeat_password" in err for err in data["detail"])


def test_register_missing_field() -> None:
    """Test validation error when a required field is missing.

    This test checks that the FastAPI form validation system correctly raises
    an HTTP 422 Unprocessable Entity error when a required field (e.g. `username`)
    is not included in the request.

    Asserts:
        - Response status code is 422.
        - The missing field is identified in the validation error details.
    """
    response = client.post(
        "/register",
        data={
            "email": "missing@example.com",
            "password": "Test1234!",
            "repeat_password": "Test1234!"
        }
    )

    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"][-1] == "username"

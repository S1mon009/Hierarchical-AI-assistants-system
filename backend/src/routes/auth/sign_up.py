"""
User registration router module.

This module defines the `router` APIRouter instance that handles user
sign-up endpoints for the FastAPI application. Currently, it provides
the `/sign-up` endpoint to register new users via form data.

The endpoint validates user input with the `SignUpModel` Pydantic model,
hashes passwords securely using bcrypt, and returns a success message.
In a production environment, the hashed password would be stored in a
database and not returned in the response.

Attributes:
    router (APIRouter): Router instance handling user registration routes,
        including the `/sign-up` endpoint.
"""
import bcrypt
from fastapi import APIRouter, Form, HTTPException
from pydantic import ValidationError
from src.models.auth import SignUpModel
from src.exceptions.form_fields import MissingFormFieldsException
from src.config import settings

router = APIRouter()
"""APIRouter: Router instance handling user sign-up routes."""


@router.post("/sign-up")
async def sign_up(
    username: str | None = Form(None),
    email: str | None = Form(None),
    password: str | None = Form(None),
    repeat_password: str | None = Form(None)
) -> dict[str, str]:
    """Register a new user.

    This endpoint processes registration requests submitted as form data.
    It validates the provided information using the `RegisterForm` Pydantic model,
    hashes the password securely using bcrypt, and returns a success message.

    If the provided data is invalid (e.g., passwords do not match, email format
    is incorrect, or fields are missing), a `400 Bad Request` error is raised
    with details about the validation issues.

    Args:
        username (str): The username chosen by the user.
        email (str): The email address provided during registration.
        password (str): The user’s password.
        repeat_password (str): The repeated password for confirmation.

    Raises:
        HTTPException: Raised with a 400 status code if validation fails,
            containing a list of validation error messages.

    Returns:
        dict[str, str]: A dictionary containing a success message with
        the hashed password (for demonstration purposes only — in a
        real application this value should not be returned).

    Example:
        ```bash
        curl -X POST "http://localhost:8000/auth/sign-up" \\
            -F "username=testuser" \\
            -F "email=test@example.com" \\
            -F "password=Secret123!" \\
            -F "repeat_password=Secret123!"
        ```

        Response:
        ```json
        {
            "message": "$2b$12$1dFSU..."
        }
        ```
    """
    try:
        fields = {
            "username": username,
            "email": email,
            "password": password,
            "repeat_password": repeat_password,
        }

        missing = [name for name, value in fields.items() if value is None]

        if missing:
            raise MissingFormFieldsException(missing)

        form = SignUpModel(
            username=username,
            email=email,
            password=password,
            repeat_password=repeat_password
        )

        password_bytes = str(form.password).encode('utf-8')
        salt = bcrypt.gensalt(rounds=settings.bcrypt_salt_rounds)
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        return {"message": hashed_password}

    except MissingFormFieldsException as e:
        raise HTTPException(
            status_code=400,
            detail=e.message
        ) from e

    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=[f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        ) from e

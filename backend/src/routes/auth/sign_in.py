"""
Authentication router module.

This module defines the `router` APIRouter instance that handles user
authentication endpoints for the FastAPI application. Currently, it
provides the `/sign-in` endpoint to authenticate existing users
using form data.

The endpoint validates user credentials with the `SignInModel` Pydantic model,
hashes passwords securely using bcrypt, and returns a success message.
In a production environment, it should verify credentials against a database
and issue authentication tokens or session cookies.

Attributes:
    router (APIRouter): Router instance handling authentication routes,
        including user sign-in.
"""
import bcrypt
from fastapi import APIRouter, Form, HTTPException
from pydantic import ValidationError
from src.models.auth import SignInModel
from src.exceptions.form_fields import MissingFormFieldsException
from src.config import settings

router = APIRouter()
"""APIRouter: Router instance handling user registration routes."""

@router.post("/sign-in")
async def sign_in(
    email: str | None = Form(None),
    password: str | None = Form(None)
) -> dict[str, str]:
    """Authenticate an existing user.

    This endpoint handles login requests submitted as form data.
    It validates the provided credentials using the `SignInModel` Pydantic model,
    securely hashes the password using bcrypt, and returns a success message.

    In a production environment, this endpoint would typically verify the
    hashed password against the database and issue a JWT token or session cookie.
    Here, the hashed password is returned for demonstration purposes only.

    Args:
        email (str): The email address associated with the user account.
        password (str): The user's plain-text password.

    Raises:
        HTTPException: Raised with a 400 status code if validation fails,
            containing a list of validation error messages.

    Returns:
        dict[str, str]: A dictionary containing a message with the hashed password
        (for demonstration purposes only — this should never be returned in production).

    Example:
        ```bash
        curl -X POST "http://localhost:8000/auth/sign-in" \
            -F "email=test@example.com" \
            -F "password=Secret123!"
        ```

        Response:
        ```json
        {
            "message": "$2b$12$kL3sR8B...hashed_password..."
        }
        ```
    """
    try:
        fields = {
            "email": email,
            "password": password,
        }

        missing = [name for name, value in fields.items() if value is None]

        if missing:
            raise MissingFormFieldsException(missing)

        form = SignInModel(
            email=email,
            password=password,
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

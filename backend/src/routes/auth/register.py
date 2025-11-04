"""User registration route for the FastAPI application.

This module defines a single endpoint responsible for handling
user registration requests. It validates form data using a
Pydantic schema, hashes passwords securely with bcrypt, and
returns a confirmation message.

The registration process is kept simple and can be extended later
to include user creation in a database or sending verification emails.

Example:
    ```python
    from fastapi import FastAPI
    from src.routes.auth import router as register_router

    app = FastAPI()
    app.include_router(register_router)
    ```
"""
import bcrypt
from fastapi import APIRouter, Form, HTTPException
from pydantic import ValidationError
from src.schemas.auth import RegisterForm
from src.config.config import settings

router = APIRouter()
"""APIRouter: Router instance handling user registration routes."""


@router.post("/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    repeat_password: str = Form(...)
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
        curl -X POST "http://localhost:8000/register" \\
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
        form = RegisterForm(
            username=username,
            email=email,
            password=password,
            repeat_password=repeat_password
        )

        password_bytes = str(form.password).encode('utf-8')
        salt = bcrypt.gensalt(rounds=settings.bcrypt_salt_rounds)
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        return {"message": hashed_password}

    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=[f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        ) from e



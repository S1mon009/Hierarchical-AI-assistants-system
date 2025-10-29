"""Authentication routes for the FastAPI application.

This module defines endpoints related to user authentication, such as registration.
"""

import bcrypt
from fastapi import APIRouter, Form, HTTPException
from pydantic import ValidationError
from src.schemas.auth import RegisterForm
from src.config.config import settings

router = APIRouter()

@router.post("/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    repeat_password: str = Form(...)
) -> dict[str, str]:
    """Handle user registration.

    Validates the registration form using the RegisterForm Pydantic model.
    Returns a success message if validation passes; otherwise raises HTTP 400
    with detailed validation errors.

    Args:
        username (str): The username provided by the user.
        email (str): The email address provided by the user.
        password (str): The password provided by the user.
        repeat_password (str): The repeated password to confirm matching.

    Raises:
        HTTPException: Raised with status code 400 if validation fails, containing
                       detailed error messages.

    Returns:
        dict: A message indicating successful registration.
    """
    try:
        form = RegisterForm(
            username=username,
            email=email,
            password=password,
            repeat_password=repeat_password
        )

        password_bytes = form.password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=settings.bcrypt_salt_rounds)
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        return {"message": hashed_password}
    except ValidationError as e:
        errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        raise HTTPException(status_code=400, detail=errors) from e

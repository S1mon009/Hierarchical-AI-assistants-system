import bcrypt
from pydantic import ValidationError
from fastapi import HTTPException
from src.modules.auth.auth_schema import SignUpSchema, SignInSchema
# from src.lib import supabase
from src.common.exceptions import MissingFormFieldsException
from src.common.security import hash_password
from src.core import config


class AuthService:
    """Service handling user authentication logic (sign-up and sign-in)."""

    @staticmethod
    def validate_missing_fields(fields: dict) -> None:
        """Check for missing form fields and raise exception if any."""
        missing = [name for name, value in fields.items() if value is None]
        if missing:
            raise MissingFormFieldsException(missing)

    async def sign_up(self, username: str, email: str, password: str, repeat_password: str) -> dict:
        """Handle the full user registration workflow."""
        try:
            # Validate missing fields
            self.validate_missing_fields({
                "username": username,
                "email": email,
                "password": password,
                "repeat_password": repeat_password,
            })

            # Validate form using Pydantic model
            form = SignUpSchema(
                username=username,
                email=email,
                password=password,
                repeat_password=repeat_password,
            )

            # Call Supabase to create user
            # result = supabase.auth.sign_up({
            #     "email": form.email,
            #     "password": form.password,
            # })

            # if not result:
            #     raise HTTPException(
            #         status_code=400,
            #         detail="Failed to register user"
            #     )

            # if result.user is None:
            #     raise HTTPException(
            #         status_code=400,
            #         detail=result.message or "Failed to register user"
            #     )

            return {"message": "User registered successfully"}

        except MissingFormFieldsException as e:
            raise HTTPException(status_code=400, detail=e.message) from e

        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail=[f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            ) from e

    async def sign_in(self, email: str, password: str) -> dict:
        """Handle user login workflow."""
        try:
            # Validate missing fields
            self.validate_missing_fields({
                "email": email,
                "password": password,
            })

            # Validate credentials
            form = SignInSchema(
                email=email,
                password=password,
            )

            return {"message": hash_password(form.password)}

        except MissingFormFieldsException as e:
            raise HTTPException(status_code=400, detail=e.message) from e

        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail=[f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            ) from e

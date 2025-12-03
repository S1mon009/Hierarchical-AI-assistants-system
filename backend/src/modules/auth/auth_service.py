from urllib.parse import urlencode
from pydantic import ValidationError
from fastapi import HTTPException, Response
from fastapi.responses import RedirectResponse
from src.modules.auth.auth_schema import SignUpSchema, SignInSchema
from src.core import supabase
from src.common.exceptions import MissingFormFieldsException
from src.core.config import config
from src.common.security.is_token_valid import is_token_valid


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
            self.validate_missing_fields({
                "username": username,
                "email": email,
                "password": password,
                "repeat_password": repeat_password,
            })

            form = SignUpSchema(
                username=username,
                email=email,
                password=password,
                repeat_password=repeat_password,
            )

            response = supabase.auth.sign_up(
                {
                    "email": form.email,
                    "password": form.password,
                    "options": {
                        "data": {
                            "display_name": form.username,
                        }
                    }
                }
            )

            if not response:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to register user"
                )

            if response.user is None:
                raise HTTPException(
                    status_code=400,
                    detail=response.message or "Failed to register user"
                )

            return {"message": "User registered successfully. Check your email for verification."}

        except MissingFormFieldsException as e:
            raise HTTPException(status_code=400, detail=e.message) from e

        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail=[f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            ) from e

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Something went wrong during registration: {str(e)}"
            ) from e

    async def sign_in(self, email: str, password: str, response: Response) -> Response:
        """Handle user login workflow."""
        try:
            self.validate_missing_fields({
                "email": email,
                "password": password,
            })

            form = SignInSchema(
                email=email,
                password=password,
            )

            res = supabase.auth.sign_in_with_password(
                {
                    "email": form.email,
                    "password": form.password,
                }
            )

            if not res or res.user is None:
                raise HTTPException(
                    status_code=400,
                    detail=res.message or "Invalid email or password"
                )

            data = {
                "access_token": res.session.access_token,
                "refresh_token": res.session.refresh_token,
                "user_id": res.user.id,
                "username": res.user.user_metadata.get("display_name"),
                "email": res.user.email
            }

            query_string = urlencode(data)

            redirect_url = f"{config.frontend_url}/auth-redirect?{query_string}"
            response.status_code = 303
            response.headers["Location"] = redirect_url
            return response

        except MissingFormFieldsException as e:
            raise HTTPException(status_code=400, detail=e.message) from e

        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail=[f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            ) from e

    async def sign_out(self, token: str) -> dict[str, str]:
        try:
            supabase.auth.admin.sign_out(token)
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to sign out: {str(e)}"
            ) from e

        return {"message": "Signed out successfully"}

    async def verify_email(self) -> dict[str, str]:
        return {"message": "Email verification successful."}

    async def google_sign_in(self) -> dict[str, str]:
        try:
            response = supabase.auth.sign_in_with_oauth(
                {
                    "provider": "google",
                    "options": {
                        "redirect_to": "http://localhost:8080/auth/google-callback"
                    }
                }
            )
            
            if not response:
                raise HTTPException(
                    status_code=400,
                    detail=response.message or "Google sign-in failed"
                )
                
            print(response)
            
            return RedirectResponse(response.url)
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Something went wrong during Google sign-in: {str(e)}"
            ) from e

    async def google_callback(self, code: str, response: Response) -> Response:
        try:
            res = supabase.auth.exchange_code_for_session({"auth_code": code})

            if not res or res.user is None:
                raise HTTPException(
                    status_code=400,
                    detail=response.message or "Google callback processing failed"
                )

            data = {
                "access_token": res.session.access_token,
                "refresh_token": res.session.refresh_token,
                "user_id": res.user.id,
                "username": res.user.user_metadata.get("display_name"),
                "email": res.user.email
            }

            query_string = urlencode(data)

            redirect_url = f"{config.frontend_url}/auth-redirect?{query_string}"
            response.status_code = 303
            response.headers["Location"] = redirect_url
            return response

        except Exception as e:
            raise HTTPException(
              status_code=500,
              detail=f"Something went wrong during Google callback processing: {str(e)}"
            ) from e

    async def get_claims(self, token: str) -> dict:
        try:
            response = supabase.auth.get_claims(token)
            if not response or response.user is None:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid token or user not found"
                )
            return {"claims": response.claims}
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve user claims: {str(e)}"
            ) from e

    async def check_and_refresh_token(self, access_token: str, refresh_token: str) -> dict:
        if access_token and is_token_valid(access_token):
            return {"access_token": access_token, "refresh_token": refresh_token}

        # Jeśli wygasł, odświeżamy przy pomocy refresh_token
        try:
            res = supabase.auth.refresh_session(refresh_token)
            if not res or res.session is None:
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            return {
                "access_token": res.session.access_token,
                "refresh_token": res.session.refresh_token
            }

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to refresh token: {str(e)}") from e

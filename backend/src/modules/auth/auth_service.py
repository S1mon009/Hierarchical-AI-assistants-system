from urllib.parse import urlencode
from pydantic import ValidationError
from fastapi import HTTPException, Response
from fastapi.responses import RedirectResponse
from src.modules.auth.auth_schema import (
    SignUpSchema,
    SignUpResponseSchema,
    SignInSchema,
    VerifyEmailResponseSchema,
    CheckAndRefreshResponseSchema,
    SignOutResponseSchema,
    GetClaimsResponseSchema
)
from src.core import supabase, config
from src.common.security import is_token_valid


class AuthService:
    async def sign_up(self, username: str, email: str, password: str, repeat_password: str) -> SignUpResponseSchema:
        """Handle the full user registration workflow."""
        try:
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

            return SignUpResponseSchema(message="User registered successfully. Check your email for verification.")

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

    async def sign_in(self, email: str, password: str) -> Response:
        """Handle user login workflow."""
        response = Response()
        try:
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

            print(data['access_token'])

            query_string = urlencode(data)

            redirect_url = f"{config.frontend_url}/auth-redirect?{query_string}"
            response.status_code = 303
            response.headers["Location"] = redirect_url
            return response

        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail=[f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            ) from e

    async def verify_email(self) -> VerifyEmailResponseSchema:
        return VerifyEmailResponseSchema(message="Email verification successful.")

    async def google_sign_in(self) -> RedirectResponse:
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

            return RedirectResponse(response.url, status_code=303)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Something went wrong during Google sign-in: {str(e)}"
            ) from e

    async def google_callback(self, code: str) -> Response:
        response = Response()
        try:
            res = supabase.auth.exchange_code_for_session({"auth_code": code})

            if not res or res.user is None:
                raise HTTPException(
                    status_code=400,
                    detail="Google callback processing failed"
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

    async def sign_out(self, token: str) -> SignOutResponseSchema:
        try:
            supabase.auth.admin.sign_out(token)
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to sign out: {str(e)}"
            ) from e

        return SignOutResponseSchema(message="Signed out successfully")

    async def check_and_refresh_token(self, access_token: str, refresh_token: str) -> CheckAndRefreshResponseSchema:
        if access_token and is_token_valid(access_token):
            return {"access_token": access_token, "refresh_token": refresh_token}

        try:
            res = supabase.auth.refresh_session(refresh_token)
            if not res or res.session is None:
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            return CheckAndRefreshResponseSchema(
                access_token=res.session.access_token,
                refresh_token=res.session.refresh_token
            )

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to refresh token: {str(e)}") from e

    async def get_claims(self, token: str) -> GetClaimsResponseSchema:
        try:
            response = supabase.auth.get_claims(token)
            if not response or response.user is None:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid token or user not found"
                )
            
            return GetClaimsResponseSchema(claims=response.claims)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve user claims: {str(e)}"
            ) from e

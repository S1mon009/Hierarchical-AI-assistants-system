from fastapi import (
    APIRouter,
    Depends,
    Query,
    Response
)
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.modules.auth.auth_service import AuthService
from src.modules.auth.auth_schema import (
    SignUpSchema,
    SignUpResponseSchema,
    SignInSchema,
    VerifyEmailResponseSchema,
    CheckAndRefreshSchema,
    CheckAndRefreshResponseSchema,
    SignOutResponseSchema,
    HealthCheckResponseSchema,
    GetClaimsResponseSchema
)


class AuthController:
    def __init__(self, auth_service: AuthService | None = None):
        self.router = APIRouter()
        self.auth_service = auth_service or AuthService()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.post(
            "/sign-up",
            response_model=SignUpResponseSchema,
            status_code=201,
            tags=["auth"],
            summary="Sign Up",
            description="Register a new user account",
            response_description="User registration successful",
            responses={
                201: {"description": "User created successfully"},
                400: {"description": "Bad request"}
            }
        )(self.sign_up)
        self.router.post(
            "/sign-in",
            status_code=200,
            tags=["auth"],
            summary="Sign In",
            description="Authenticate user",
            response_description="Authentication successful",
            responses={
                200: {"description": "Login successful"},
                401: {"description": "Unauthorized"}
            }
        )(self.sign_in)
        self.router.get(
            "/verify-email",
            response_model=VerifyEmailResponseSchema,
            status_code=200,
            tags=["auth"],
            summary="Verify Email",
            description="Verify user email",
            response_description="Email verified",
            responses={
                200: {"description": "Email verified"},
                400: {"description": "Invalid token"}
            }
        )(self.verify_email)
        self.router.get(
            "/google-sign-in",
            status_code=302,
            tags=["auth"],
            summary="Google Sign In",
            description="Initiate Google OAuth sign in",
            response_description="Redirect to Google",
            responses={
                302: {"description": "Redirect to Google OAuth"}
            }
        )(self.google_sign_in)
        self.router.get(
            "/google-callback",
            status_code=200,
            tags=["auth"],
            summary="Google Callback",
            description="Handle Google OAuth callback",
            response_description="Authentication successful",
            responses={
                200: {"description": "Login successful"},
                400: {"description": "Bad request"}
            }
        )(self.google_callback)
        self.router.post(
            "/sign-out",
            response_model=SignOutResponseSchema,
            status_code=200,
            tags=["auth"],
            summary="Sign Out",
            description="Sign out user",
            response_description="Sign out successful",
            responses={
                200: {"description": "Sign out successful"},
                401: {"description": "Unauthorized"}
            }
        )(self.sign_out)
        self.router.post(
            "/check-token",
            response_model=CheckAndRefreshResponseSchema,
            status_code=200,
            tags=["auth"],
            summary="Check and Refresh Token",
            description="Check token validity and refresh if needed",
            response_description="Token checked and refreshed",
            responses={
                200: {"description": "Token refreshed"},
                401: {"description": "Unauthorized"}
            }
        )(self.check_and_refresh_token)
        self.router.get(
            "/claims",
            response_model=GetClaimsResponseSchema,
            status_code=200,
            tags=["auth"],
            summary="Get Claims",
            description="Get user claims from token",
            response_description="User claims",
            responses={
                200: {"description": "Claims retrieved"},
                401: {"description": "Unauthorized"}
            }
        )(self.get_claims)
        self.router.get(
            "/health",
            response_model=HealthCheckResponseSchema,
            status_code=200,
            tags=["health"],
            summary="Health Check",
            description="Check service health",
            response_description="Service is healthy",
            responses={
                200: {"description": "Service is healthy"}
            }
        )(self.health_check)

    async def sign_up(
        self, data: SignUpSchema
    ) -> SignUpResponseSchema:
        return await self.auth_service.sign_up(
            data.username, 
            data.email,
            data.password,
            data.repeat_password
        )

    async def sign_in(
        self,
        data: SignInSchema
    ) -> Response:
        return await self.auth_service.sign_in(data.email, data.password)

    async def verify_email(self) -> VerifyEmailResponseSchema:
        return await self.auth_service.verify_email()

    async def google_sign_in(self) -> RedirectResponse:
        return await self.auth_service.google_sign_in()

    async def google_callback(self, code: str = Query(..., description="Authentication code")) -> Response:
        return await self.auth_service.google_callback(code)

    async def sign_out(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> SignOutResponseSchema:
        token = credentials.credentials
        return await self.auth_service.sign_out(token)

    async def check_and_refresh_token(
        self, data: CheckAndRefreshSchema
    ) -> CheckAndRefreshResponseSchema:
        return await self.auth_service.check_and_refresh_token(data.access_token, data.refresh_token)

    async def get_claims(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> GetClaimsResponseSchema:
        token = credentials.credentials
        return await self.auth_service.get_claims(token)

    async def health_check(self) -> HealthCheckResponseSchema:
        return {"status": "ok"}

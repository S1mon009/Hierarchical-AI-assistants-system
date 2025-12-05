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
        self.router.post("/sign-up", response_model=SignUpResponseSchema)(self.sign_up)
        self.router.post("/sign-in")(self.sign_in)
        self.router.get("/verify-email", response_model=VerifyEmailResponseSchema)(self.verify_email)
        self.router.get("/google-sign-in")(self.google_sign_in)
        self.router.get("/google-callback")(self.google_callback)
        self.router.post("/sign-out", response_model=SignOutResponseSchema)(self.sign_out)
        self.router.post("/check-token", response_model=CheckAndRefreshResponseSchema)(self.check_and_refresh_token)
        self.router.get("/claims", response_model=GetClaimsResponseSchema)(self.get_claims)
        self.router.get("/health", response_model=HealthCheckResponseSchema)(self.health_check)

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

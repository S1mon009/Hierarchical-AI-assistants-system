from fastapi import APIRouter, Form, Depends, Query, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.modules.auth.auth_service import AuthService

router = APIRouter()
"""APIRouter: Router instance handling user sign-up routes."""
auth_service = AuthService()


@router.post("/sign-up")
async def sign_up(
    username: str | None = Form(None),
    email: str | None = Form(None),
    password: str | None = Form(None),
    repeat_password: str | None = Form(None)
) -> dict[str, str]:
    return await auth_service.sign_up(username, email, password, repeat_password)

@router.post("/sign-in")
async def sign_in(
    email: str | None = Form(None),
    password: str | None = Form(None)
) -> Response:
    return await auth_service.sign_in(email, password, response=Response())

@router.get("/verify-email")
async def verify_email() -> dict[str, str]:
    return await auth_service.verify_email()

@router.get("/google-sign-in")
async def google_sign_in() -> dict[str, str]:
    return await auth_service.google_sign_in()

@router.get("/google-callback")
async def google_callback(code: str = Query(...)) -> Response:
    return await auth_service.google_callback(code, response=Response())

@router.post("/sign-out")
async def sign_out(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> dict[str, str]:
    token = credentials.credentials
    return await auth_service.sign_out(token)

@router.post("/check-token")
async def check_and_refresh_token(access_token: str, refresh_token: str):
    return await auth_service.check_and_refresh_token(access_token, refresh_token)

@router.get('/health')
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
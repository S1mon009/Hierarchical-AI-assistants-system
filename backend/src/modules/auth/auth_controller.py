from fastapi import APIRouter, Form
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
) -> dict[str, str]:
    return await auth_service.sign_in(email, password)

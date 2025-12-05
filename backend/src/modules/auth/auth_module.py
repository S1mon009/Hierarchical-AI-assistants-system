from fastapi import APIRouter
from src.modules.auth.auth_controller import AuthController

class AuthModule:
    def __init__(self):
        self.router = APIRouter()
        self.router.include_router(AuthController().router, prefix="/auth", tags=["Auth"])

auth_module = AuthModule()

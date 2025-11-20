from fastapi import APIRouter
from src.modules.auth.auth_controller import router as auth_routes

class AuthModule:
    def __init__(self):
        self.router = APIRouter()
        self.router.include_router(auth_routes, prefix="/auth", tags=["Auth"])

auth_module = AuthModule()

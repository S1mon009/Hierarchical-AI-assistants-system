from fastapi import APIRouter
from src.modules.users.users_controller import UsersController

class UsersModule:
    def __init__(self):
        self.router = APIRouter()
        self.router.include_router(UsersController().router, prefix="/users", tags=["Users"])

users_module = UsersModule()

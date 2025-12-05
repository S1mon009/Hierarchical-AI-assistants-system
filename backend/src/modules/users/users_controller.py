from fastapi import (
    APIRouter,
    Query
)
from src.modules.users.users_service import UsersService
from src.modules.users.users_schema import RetrieveUserResponseModel

class UsersController:
    def __init__(self, users_service: UsersService | None = None):
        self.router = APIRouter()
        self.users_service = users_service or UsersService()
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.get("/me", response_model=RetrieveUserResponseModel)(self.retrieve_user)

    async def retrieve_user(
        self,
        token: str = Query(..., description="Authentication token")
    ) -> RetrieveUserResponseModel:
        return await self.users_service.retrieve_user(token)

users_router = UsersController().router

from fastapi import HTTPException
from src.modules.users.users_schema import RetrieveUserResponseModel
from src.core import supabase

class UsersService:
    async def retrieve_user(self, token: str) -> RetrieveUserResponseModel:
        try:
            response = supabase.auth.get_user(token)
            if not response or response.user is None:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid token or user not found"
                )
            return RetrieveUserResponseModel(**response.user.dict())
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve user: {str(e)}"
            ) from e

from fastapi import APIRouter, Depends
from fastapi import APIRouter, Depends, UploadFile
from src.modules.auth.dependencies import get_current_user
from src.modules.upload.upload_service import UploadService

class UploadController:
    def __init__(self, service: UploadService):
        self.router = APIRouter()
        self.service = service
        self._routes()

    def _routes(self) -> None:
        self.router.post(
            "/google-credentials",
            status_code=200,
            tags=["upload"],
            summary="Summary",
            description="Description"
        )(self.upload_google_credentials)

    async def upload_google_credentials(self, file: UploadFile, user=Depends(get_current_user)):
        return await self.service.upload_google_credentials(file, user.id)

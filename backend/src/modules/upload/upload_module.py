from fastapi import APIRouter
from src.core.db import supabase
from src.modules.upload.upload_controller import UploadController
from src.modules.upload.upload_service import UploadService
from src.modules.chat.repositories.google_credentials_repository import GoogleCredentialsRepository

class UploadModule:
    def __init__(self):
        repo = GoogleCredentialsRepository(supabase)
        service = UploadService(repo)
        controller = UploadController(service)
        self.router = APIRouter()
        self.router.include_router(
            controller.router,
            prefix="/upload",
            tags=["upload"]
        )

upload_module = UploadModule()

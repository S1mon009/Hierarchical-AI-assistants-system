from uuid import UUID
import json
from fastapi import HTTPException, Response, UploadFile
from fastapi.responses import RedirectResponse
from src.modules.chat.repositories.google_credentials_repository import GoogleCredentialsRepository
from pydantic import ValidationError

class UploadService:
    def __init__(self, repo: GoogleCredentialsRepository):
        self.repo = repo

    async def upload_google_credentials(self, file: UploadFile, user_id: UUID):
        if not file.filename.endswith(".json"):
            raise HTTPException(status_code=400, detail="File must be a JSON file")
        content = await file.read()
        try:
            credentials = json.loads(content)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON file")

        self.repo.save_credentials(user_id, credentials)
        return {"message": "Google credentials uploaded successfully"}
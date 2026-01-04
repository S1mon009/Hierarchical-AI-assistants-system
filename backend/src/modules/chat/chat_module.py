from fastapi import APIRouter
from src.core.db import supabase
from src.modules.chat.chat_controller import ChatController
from src.modules.chat.chat_service import ChatService
from src.modules.chat.chat_repository import ChatRepository

class ChatModule:
    def __init__(self):
        repo = ChatRepository(supabase)
        service = ChatService(repo)
        controller = ChatController(service)

        self.router = APIRouter()
        self.router.include_router(controller.router, prefix="/chat", tags=["Chat"])

chat_module = ChatModule()

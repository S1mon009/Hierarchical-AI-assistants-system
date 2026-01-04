from fastapi import APIRouter, Depends, Request
from uuid import UUID
from src.modules.chat.chat_service import ChatService
from src.modules.chat.chat_schema import CreateChatSchema, SendMessageSchema
from src.modules.chat.dependencies import get_current_user
from fastapi.responses import StreamingResponse

class ChatController:
    def __init__(self, service: ChatService):
        self.router = APIRouter()
        self.service = service
        self._routes()

    def _routes(self):
        self.router.get("/chats")(self.list_chats)
        self.router.post("/")(self.create_chat)
        self.router.post("/{chat_id}/messages")(self.send_message)
        self.router.post("/{chat_id}/stream")(self.stream_message)
        self.router.get("/{chat_id}")(self.get_chat)

    async def create_chat(self, data: CreateChatSchema, user=Depends(get_current_user)):
        return await self.service.create_chat(user.id, data.message)

    async def send_message(self, chat_id: UUID, data: SendMessageSchema, user=Depends(get_current_user)):
        messages = await self.service.send_message(chat_id, user.id, data.message)
        return {"chat_id": chat_id, "messages": messages}

    async def stream_message(self, chat_id: UUID, request: Request, user=Depends(get_current_user)):
        data = await request.json()
        user_message = data.get("message")
        return await self.service.stream_response(chat_id, user_message)

    async def get_chat(self, chat_id: UUID, user=Depends(get_current_user)):
        messages = self.service.repo.get_messages(chat_id)
        chat = self.service.repo.get_chat(chat_id, user.id)
        return {"chat_id": chat_id, "title": chat.get("title"), "messages": messages}

    async def list_chats(self, user=Depends(get_current_user)):
        return self.service.repo.list_chats(user.id)

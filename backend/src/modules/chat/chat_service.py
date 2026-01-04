import json
import asyncio
from uuid import UUID
from fastapi.responses import StreamingResponse
from src.modules.chat.chat_repository import ChatRepository
from .agents.main_agent import MainAgent

class ChatService:
    def __init__(self, repo: ChatRepository):
        self.repo = repo
        self.agent = MainAgent()

    async def create_chat(self, user_id: UUID, user_message: str):
        chat = self.repo.create_chat(user_id, user_message[:60])
        chat_id = chat["id"]
        self.repo.add_message(chat_id, "user", user_message)
        return chat

    async def send_message(self, chat_id: UUID, user_id: UUID, user_message: str):
        messages = self.repo.get_messages(chat_id)
        history = [{"role": m["role"], "content": m["content"]} for m in messages]

        history.append({"role": "user", "content": user_message})
        self.repo.add_message(chat_id, "user", user_message)

        ai_response = self.agent.invoke(history).content
        self.repo.add_message(chat_id, "assistant", ai_response)

        return self.repo.get_messages(chat_id)

    async def stream_response(self, chat_id: UUID, user_message: str):
        messages = self.repo.get_messages(chat_id)
        history = [{"role": m["role"], "content": m["content"]} for m in messages]

        history.append({"role": "user", "content": user_message})
        self.repo.add_message(chat_id, "user", user_message)

        async def event_generator():
            ai_response = self.agent.invoke(history).content
            self.repo.add_message(chat_id, "assistant", ai_response)

            chunk_size = 50
            for i in range(0, len(ai_response), chunk_size):
                yield json.dumps({"role": "assistant", "content": ai_response[i:i+chunk_size]}) + "\n"
                await asyncio.sleep(0.05)

        return StreamingResponse(event_generator(), media_type="application/json")

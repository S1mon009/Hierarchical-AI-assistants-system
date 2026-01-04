from pydantic import BaseModel
from typing import Literal, List
from uuid import UUID
from datetime import datetime

Role = Literal["system", "user", "assistant", "tool"]

class ChatMessageSchema(BaseModel):
    role: Role
    content: str

class CreateChatSchema(BaseModel):
    message: str

class SendMessageSchema(BaseModel):
    message: str

class ChatSchema(BaseModel):
    id: UUID
    title: str | None
    messages: List[ChatMessageSchema]
    created_at: datetime

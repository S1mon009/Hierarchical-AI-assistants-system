from uuid import UUID
from typing import List

class ChatRepository:
    def __init__(self, supabase):
        self.supabase = supabase

    def create_chat(self, user_id: UUID, title: str) -> dict:
        res = self.supabase.table("ai_chats").insert({
            "user_id": str(user_id),
            "title": title
        }).execute()
        return res.data[0]

    def add_message(self, chat_id: UUID, role: str, content: str) -> dict:
        res = self.supabase.table("ai_chat_messages").insert({
            "chat_id": str(chat_id),
            "role": role,
            "content": content
        }).execute()
        return res.data[0]

    def get_messages(self, chat_id: UUID) -> List[dict]:
        res = self.supabase.table("ai_chat_messages") \
            .select("*") \
            .eq("chat_id", str(chat_id)) \
            .order("created_at") \
            .execute()
        return res.data

    def get_chat(self, chat_id: UUID, user_id: UUID) -> dict:
        res = self.supabase.table("ai_chats") \
            .select("*") \
            .eq("id", str(chat_id)) \
            .eq("user_id", str(user_id)) \
            .single() \
            .execute()
        return res.data

    def list_chats(self, user_id: UUID) -> List[dict]:
        res = self.supabase.table("ai_chats") \
            .select("id, title, created_at, updated_at") \
            .eq("user_id", str(user_id)) \
            .order("updated_at", desc=True) \
            .execute()
        return res.data

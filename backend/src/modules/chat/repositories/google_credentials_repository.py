from src.core.db import supabase
from uuid import UUID
import json, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from os import getenv

SECRET_KEY = base64.b64decode(getenv("GOOGLE_CREDENTIALS_KEY"))

def encrypt_data(data: dict) -> str:
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(json.dumps(data).encode(), AES.block_size))
    return base64.b64encode(cipher.iv + ct_bytes).decode()

def decrypt_data(enc_str: str) -> dict:
    raw = base64.b64decode(enc_str)
    iv = raw[:16]
    ct = raw[16:]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    return json.loads(unpad(cipher.decrypt(ct), AES.block_size).decode())

class GoogleCredentialsRepository:
    def get_credentials(self, user_id: UUID) -> dict | None:
        res = supabase.table("google_credentials") \
            .select("credentials") \
            .eq("user_id", str(user_id)) \
            .single() \
            .execute()
        if not res.data:
            return None
        return decrypt_data(res.data["credentials"])

    def save_credentials(self, user_id: UUID, credentials: dict):
        enc = encrypt_data(credentials)
        supabase.table("google_credentials") \
            .upsert({"user_id": str(user_id), "credentials": enc}, on_conflict="user_id") \
            .execute()

    def has_credentials(self, user_id: UUID) -> bool:
        res = supabase.table("google_credentials") \
            .select("credentials") \
            .eq("user_id", str(user_id)) \
            .single() \
            .execute()
        return bool(res.data)

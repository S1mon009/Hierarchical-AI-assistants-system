from fastapi import Depends, HTTPException, Header
from src.core.db import supabase

async def get_supabase():
    return supabase

async def get_current_user(
    authorization: str = Header(...),
    supabase_client = Depends(get_supabase)
):
    token = authorization.replace("Bearer ", "")
    user_resp = supabase_client.auth.get_user(token)

    if not user_resp or not user_resp.user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user_resp.user

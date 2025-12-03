from supabase import create_client, Client
from src.core import config

supabase: Client = create_client(config.supabase_url, config.supabase_key)

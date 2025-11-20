from supabase import create_client, Client
from src.core import config

supabase_client: Client = create_client(config.supabase_url, config.supabase_service_role_key)

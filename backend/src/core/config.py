from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    host: str
    port: int
    bcrypt_salt_rounds: int
    supabase_url: str
    supabase_key: str
    supabase_anon_key: str
    supabase_service_role_key: str
    frontend_url: str
    openrouter_api_key: str
    openrouter_url: str
    max_chat_history: int
    stream_timeout: int
    title_generation_prompt: str

    model_config = SettingsConfigDict(env_file=".env")

config = Config()

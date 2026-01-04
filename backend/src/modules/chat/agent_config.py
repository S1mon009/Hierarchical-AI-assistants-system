from pydantic_settings import BaseSettings
from functools import lru_cache

class AgentSettings(BaseSettings):
    """Configuration for AI agents - extends main config."""
    
    # Agent settings
    max_chat_history: int = 50
    stream_timeout: int = 30
    title_generation_prompt: str = "Generate a short, concise title (max 6 words) for this conversation"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_agent_settings() -> AgentSettings:
    """Get cached agent settings instance."""
    return AgentSettings()
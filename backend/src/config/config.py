from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host: str
    port: int

    class Config:
        env_file: str = ".env"

settings = Settings()

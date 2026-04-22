from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Virtual Friend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # SQLite для разработки
    DATABASE_URL: str = "sqlite+aiosqlite:///./virtual_friend.db"

    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
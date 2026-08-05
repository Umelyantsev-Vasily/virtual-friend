from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')


# SQLite (рабочий вариант)
# DATABASE_URL: str = "sqlite+aiosqlite:///./virtual_friend.db"

class Settings(BaseSettings):
    APP_NAME: str = "Virtual Friend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"  # development / production

    # База данных — выбирается автоматически
    DATABASE_URL: str = ""

    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = ""
    TELEGRAM_BOT_TOKEN: str = ""

    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Автоматический выбор БД
        if not self.DATABASE_URL:
            if self.ENVIRONMENT == "production":
                self.DATABASE_URL = "postgresql+asyncpg://friend:friend123@localhost:5432/virtual_friend"
            else:
                self.DATABASE_URL = "sqlite+aiosqlite:///./virtual_friend.db"


settings = Settings()
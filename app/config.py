from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')


class Settings(BaseSettings):
    APP_NAME: str = "Virtual Friend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # PostgreSQL (через Docker)
#    DATABASE_URL: str = "postgresql+asyncpg://friend:friend123@localhost:5432/virtual_friend"
    # SQLite (рабочий вариант)
    DATABASE_URL: str = "sqlite+aiosqlite:///./virtual_friend.db"

    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = ""
    TELEGRAM_BOT_TOKEN: str = "8644088312:AAH364eBNzLj32ZJ1-hJpEGXkgxeKVT5yU8"

    # DeepSeek API Configuration
    DEEPSEEK_API_KEY: str = "sk-86b94c7c09354cfbbba24e265e4ec9e5"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
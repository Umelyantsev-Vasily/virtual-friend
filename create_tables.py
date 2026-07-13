import asyncio
from sqlalchemy import create_engine, text
from app.config import settings
from app.core.database import Base

# Синхронный движок для PostgreSQL
sync_engine = create_engine(
    settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
)

def create_tables():
    print("🔧 Создаём таблицы...")
    Base.metadata.create_all(sync_engine)
    print("✅ Таблицы созданы!")

if __name__ == "__main__":
    create_tables()
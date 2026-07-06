import asyncio
from app.core.database import engine, Base
from app.models import character, message

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База данных создана с правильной структурой")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())

import asyncio
import asyncpg
import sys

async def test():
    print("1. Пытаемся подключиться через asyncpg...")
    try:
        conn = await asyncpg.connect(
            user='postgres',
            password='221096',
            database='virtual_friend',
            host='localhost',
            port=5432,
            timeout=5
        )
        print("✅ Подключение через asyncpg успешно!")
        await conn.close()
    except Exception as e:
        print(f"❌ Ошибка asyncpg: {e}")
        print(f"Тип ошибки: {type(e)}")

asyncio.run(test())
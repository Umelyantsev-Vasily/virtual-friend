# test_connection.py
import asyncio
import asyncpg


async def test():
    try:
        # Прямое подключение
        conn = await asyncpg.connect(
            user="friend",
            password="221096",
            database="virtual_friend",  # Важно: указываем базу!
            host="localhost",
            port=5432
        )
        result = await conn.fetch("SELECT 1")
        print("✅ Прямое подключение успешно!")
        print(f"   Результат: {result[0][0]}")

        # Проверяем версию
        version = await conn.fetch("SELECT version()")
        print(f"   PostgreSQL: {version[0][0][:50]}...")

        # Проверяем расширение vector
        vector = await conn.fetch("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
        if vector:
            print(f"   pgvector: {vector[0][0]}")
        else:
            print("   ❌ pgvector не установлен!")

        await conn.close()
        return True

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


async def test_sqlalchemy():
    """Тест через SQLAlchemy"""
    try:
        from app.core.database import AsyncSessionLocal
        from sqlalchemy import text

        async with AsyncSessionLocal() as session:
            result = await session.execute(text('SELECT 1'))
            print("✅ SQLAlchemy подключение успешно!")
            print(f"   Результат: {result.scalar()}")
            return True
    except Exception as e:
        print(f"❌ Ошибка SQLAlchemy: {e}")
        return False


async def main():
    print("🔍 Тестируем подключение к PostgreSQL...")
    print("=" * 50)

    print("\n1️⃣ Прямое подключение через asyncpg:")
    direct = await test()

    print("\n2️⃣ Подключение через SQLAlchemy:")
    sa = await test_sqlalchemy()

    print("\n" + "=" * 50)
    if direct and sa:
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    else:
        print("❌ ЕСТЬ ПРОБЛЕМЫ С ПОДКЛЮЧЕНИЕМ!")


if __name__ == "__main__":
    asyncio.run(main())
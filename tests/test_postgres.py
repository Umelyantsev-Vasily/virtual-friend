# test_postgres.py
import asyncio
from app.core.database import AsyncSessionLocal
from sqlalchemy import text


async def test_connection():
    """Проверка подключения к PostgreSQL"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text('SELECT 1'))
            print('✅ Подключение к PostgreSQL успешно!')
            print(f'Результат: {result.scalar()}')

            # Проверяем таблицы
            tables = await session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables_list = [row[0] for row in tables.fetchall()]
            print(f'📊 Таблицы в базе: {tables_list}')

            # Проверяем структуру memories
            columns = await session.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'memories'
                ORDER BY ordinal_position
            """))
            print('\n📋 Структура таблицы memories:')
            for col in columns.fetchall():
                print(f'  • {col[0]}: {col[1]}')

    except Exception as e:
        print(f'❌ Ошибка: {e}')


if __name__ == "__main__":
    asyncio.run(test_connection())
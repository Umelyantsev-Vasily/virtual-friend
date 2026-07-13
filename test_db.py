import asyncio
import asyncpg

async def test():
    try:
        conn = await asyncpg.connect(
            user='friend',
            password='friend123',
            database='virtual_friend',
            host='host.docker.internal',
            port=5432
        )
        result = await conn.fetch('SELECT 1')
        print('✅ Подключение к PostgreSQL успешно!')
        await conn.close()
    except Exception as e:
        print(f'❌ Ошибка: {e}')

asyncio.run(test())
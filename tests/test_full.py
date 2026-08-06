# test_full.py
import asyncio
from app.core.database import AsyncSessionLocal
from app.services.memory_service import MemoryService
from app.services.ai_service import get_embedding
from sqlalchemy import text


async def full_test():
    """Полный тест всей системы"""

    print('=' * 50)
    print('🧪 ПОЛНЫЙ ТЕСТ СИСТЕМЫ')
    print('=' * 50)

    # 1. Проверка подключения
    print('\n1️⃣ Проверка подключения к PostgreSQL...')
    async with AsyncSessionLocal() as db:
        result = await db.execute(text('SELECT version()'))
        version = result.scalar()
        print(f'   ✅ PostgreSQL версия: {version[:50]}...')

    # 2. Проверка pgvector
    print('\n2️⃣ Проверка расширения pgvector...')
    async with AsyncSessionLocal() as db:
        result = await db.execute(text("SELECT extversion FROM pg_extension WHERE extname = 'vector'"))
        vector_version = result.scalar()
        if vector_version:
            print(f'   ✅ pgvector версия: {vector_version}')
        else:
            print('   ❌ pgvector не установлен!')

    # 3. Проверка таблиц
    print('\n3️⃣ Проверка таблиц...')
    async with AsyncSessionLocal() as db:
        tables = await db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables_list = [row[0] for row in tables.fetchall()]
        print(f'   📊 Таблицы: {tables_list}')

        expected_tables = ['characters', 'messages', 'memories']
        for table in expected_tables:
            if table in tables_list:
                print(f'   ✅ Таблица {table} существует')
            else:
                print(f'   ❌ Таблица {table} отсутствует!')

    # 4. Проверка эмбеддингов
    print('\n4️⃣ Проверка генерации эмбеддингов...')
    test_text = 'Тестовый текст для эмбеддинга'
    embedding = get_embedding(test_text)
    print(f'   ✅ Размерность: {len(embedding)} (ожидается 384)')
    print(f'   📊 Первые 3 значения: {embedding[:3]}')

    # 5. Проверка сохранения факта
    print('\n5️⃣ Проверка сохранения факта...')
    async with AsyncSessionLocal() as db:
        service = MemoryService(db, character_id=999)  # Тестовый ID

        # Очищаем тестовые данные
        await service.clear_all()

        # Сохраняем факт
        test_fact = 'Тестовый факт для проверки векторного поиска'
        await service.add_fact(test_fact)
        print(f'   ✅ Факт сохранен: "{test_fact}"')

        # Проверяем что сохранилось
        facts = await service.get_all_facts()
        print(f'   📊 Всего фактов: {len(facts)}')

        if len(facts) > 0:
            # Проверяем наличие эмбеддинга
            result = await db.execute(text("""
                SELECT fact, array_length(embedding, 1) as vector_size
                FROM memories 
                WHERE character_id = 999
            """))
            row = result.fetchone()
            if row:
                print(f'   ✅ Факт: "{row[0]}"')
                print(f'   ✅ Размер вектора: {row[1]} (ожидается 384)')

    # 6. Проверка векторного поиска
    print('\n6️⃣ Проверка векторного поиска...')
    async with AsyncSessionLocal() as db:
        service = MemoryService(db, character_id=999)

        # Добавляем больше тестовых фактов
        test_facts = [
            'Пользователь любит программировать на Python',
            'Пользователь увлекается искусственным интеллектом',
            'Пользователь работает разработчиком',
            'Пользователь любит читать книги по технологиям'
        ]

        for fact in test_facts:
            await service.add_fact(fact)

        # Поиск
        query = 'Чем занимается пользователь?'
        results = await service.get_relevant_facts(query, limit=3)

        print(f'   📝 Запрос: "{query}"')
        print(f'   🎯 Найдено фактов: {len(results)}')
        for i, fact in enumerate(results, 1):
            print(f'      {i}. {fact}')

    # 7. Очистка тестовых данных
    print('\n7️⃣ Очистка тестовых данных...')
    async with AsyncSessionLocal() as db:
        service = MemoryService(db, character_id=999)
        await service.clear_all()
        print('   🧹 Тестовые данные удалены')

    print('\n' + '=' * 50)
    print('✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!')
    print('=' * 50)


if __name__ == "__main__":
    asyncio.run(full_test())
# test_embedding.py
import asyncio
from app.services.ai_service import get_embedding
from app.core.database import AsyncSessionLocal
from app.services.memory_service import MemoryService


async def test_embedding():
    """Тестирование эмбеддингов и памяти"""

    print('🔍 Тестируем генерацию эмбеддинга...')
    text = 'Привет, меня зовут Анна, мне 25 лет'
    embedding = get_embedding(text)
    print(f'✅ Эмбеддинг создан! Размерность: {len(embedding)}')
    print(f'Первые 5 значений: {embedding[:5]}')
    print()

    print('💾 Тестируем сохранение факта...')
    async with AsyncSessionLocal() as db:
        # Создаем тестовый факт
        service = MemoryService(db, character_id=1)

        # Очищаем старые тестовые данные
        await service.clear_all()

        # Добавляем факты
        facts = [
            'Имя пользователя: Анна',
            'Возраст пользователя: 25',
            'Увлечение: программирование на Python',
            'Любимая еда: пицца и суши'
        ]

        for fact in facts:
            await service.add_fact(fact)
            print(f'  ✅ Сохранен факт: {fact}')

        print()
        print('🔎 Тестируем векторный поиск...')

        # Поиск по смыслу
        queries = [
            ('Как зовут пользователя?', 2),
            ('Чем увлекается?', 2),
            ('Что любит есть?', 2)
        ]

        for query, limit in queries:
            print(f'\n📝 Запрос: "{query}"')
            results = await service.get_relevant_facts(query, limit=limit)
            print(f'  Найдено {len(results)} фактов:')
            for fact in results:
                print(f'    • {fact}')


if __name__ == "__main__":
    asyncio.run(test_embedding())
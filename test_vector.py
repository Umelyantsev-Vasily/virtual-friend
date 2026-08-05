# test_vector.py
import asyncio
from app.core.database import AsyncSessionLocal
from app.services.memory_service import MemoryService


async def test():
    async with AsyncSessionLocal() as db:
        service = MemoryService(db, character_id=1)

        # Добавляем факт
        await service.add_fact("Пользователь любит кофе", [0.1] * 384)
        await service.add_fact("Пользователь любит пиццу", [0.2] * 384)
        await service.add_fact("Пользователь любит чай", [0.3] * 384)

        # Поиск
        query = [0.15] * 384
        results = await service.get_relevant_facts(query, limit=2)
        print("Найденные факты:", results)


asyncio.run(test())
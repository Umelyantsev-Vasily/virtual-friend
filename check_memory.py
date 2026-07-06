import asyncio
from app.core.database import AsyncSessionLocal
from app.services.character_service import CharacterService
from app.services.memory_service import MemoryService


async def check_memory():
    telegram_id = '1155154299'  # твой Telegram ID

    async with AsyncSessionLocal() as db:
        service = CharacterService(db)
        character = await service.get_by_user_id(telegram_id)

        if not character:
            print("❌ Персонаж не найден")
            return

        print(f"👤 Персонаж: {character.name}")
        print(f"🆔 ID: {character.id}")
        print(f"📅 Возраст: {character.age}")
        print(f"🧬 Характер: {character.personality}")
        print()

        # Проверяем память
        memory = MemoryService(character.id)
        facts = await memory.get_all_facts()

        print(f"🧠 Фактов в памяти: {len(facts)}")
        if facts:
            print("📋 Список фактов:")
            for fact in facts:
                print(f"  • {fact}")
        else:
            print("  ❌ Фактов нет")

        # Проверяем поиск
        print()
        print("🔍 Поиск по запросу 'Что я люблю?':")
        results = await memory.get_relevant_facts('Что я люблю?', limit=3)
        if results:
            for fact in results:
                print(f"  • {fact}")
        else:
            print("  ❌ Ничего не найдено")


if __name__ == "__main__":
    asyncio.run(check_memory())
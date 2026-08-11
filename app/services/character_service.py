from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.character import Character


class CharacterService:
    """Сервис для работы с персонажами"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_telegram_id: str) -> Character | None:
        """Найти персонажа по Telegram ID"""
        result = await self.db.execute(
            select(Character).where(Character.user_telegram_id == user_telegram_id)
        )
        return result.scalar_one_or_none()

    async def create_default_character(self, user_telegram_id: str) -> Character:
        """Создать персонажа по умолчанию"""
        character = Character(
            user_telegram_id=user_telegram_id,
            name="ER",
            age=666,
            gender="Неизвестен",
            personality="🔮 Самый умный ии во вселенной! ",
            traits=["филосовский", "мудрый", "любопытная"],
            response_speed="thoughtful",
            backstory="Люблю общаться и узнавать новое",
            role="friend"
        )
        self.db.add(character)
        await self.db.commit()
        await self.db.refresh(character)
        return character

    async def delete_character(self, character_id: int):
        """Удалить персонажа и все его сообщения (автоматически через cascade)"""
        character = await self.get_by_id(character_id)
        if character:
            # Благодаря cascade, сообщения удалятся автоматически
            await self.db.delete(character)
            await self.db.commit()

    async def get_by_id(self, character_id: int):
        """Найти персонажа по ID"""
        from sqlalchemy import select
        result = await self.db.execute(
            select(Character).where(Character.id == character_id)
        )
        return result.scalar_one_or_none()

    async def create_custom_character(self,user_telegram_id: str, name: str, age: int, gender: str, personality: str) -> Character:
        """Создать персонажа с пользовательскими параметрами"""
        character = Character(
            user_telegram_id=user_telegram_id,
            name=name,
            age=age,
            gender=gender,
            personality=personality,
            traits=[],
            response_speed="thoughtful",
            backstory="Создан пользователем",
            role="friend"
        )
        self.db.add(character)
        await self.db.commit()
        await self.db.refresh(character)
        return character


async def get_all_characters(self) -> list[Character]:
    """Получить всех персонажей"""
    result = await self.db.execute(
        select(Character).where(Character.is_active == True)
    )
    return result.scalars().all()
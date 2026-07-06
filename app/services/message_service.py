from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message


class MessageService:
    """Сервис для работы с сообщениями"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_user_message(self, character_id: int, content: str) -> Message:
        """Сохранить сообщение пользователя"""
        message = Message(
            character_id=character_id,
            role="user",
            content=content
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def save_assistant_message(self, character_id: int, content: str) -> Message:
        """Сохранить ответ ассистента"""
        message = Message(
            character_id=character_id,
            role="assistant",
            content=content
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_history(self, character_id: int, limit: int = 50) -> list[Message]:
        """Получить историю сообщений"""
        from sqlalchemy import select
        result = await self.db.execute(
            select(Message)
            .where(Message.character_id == character_id)
            .order_by(Message.created_at)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_history_for_ai(self, character_id: int, limit: int = 10) -> list:
        """Получить историю сообщений для AI в формате OpenAI API"""
        result = await self.db.execute(
            select(Message)
            .where(Message.character_id == character_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
        )
        messages = result.scalars().all()
        messages.reverse()  # чтобы было от старого к новому

        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

    async def get_full_context(self, character_id: int, limit: int = 20) -> list:
        """Получить расширенную историю (20 сообщений)"""
        return await self.get_history_for_ai(character_id, limit)
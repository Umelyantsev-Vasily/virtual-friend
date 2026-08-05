from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.memory import Memory
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class MemoryService:
    def __init__(self, db: AsyncSession, character_id: int):
        self.db = db
        self.character_id = character_id

    async def add_fact(self, fact: str, embedding: list = None):
        """Сохранить факт с вектором"""
        memory = Memory(
            character_id=self.character_id,
            fact=fact,
            embedding=embedding if embedding else None
        )
        self.db.add(memory)
        await self.db.commit()

    async def get_relevant_facts(self, query_embedding: list, limit: int = 5) -> list[str]:
        """
        Векторный поиск фактов по смыслу (только для PostgreSQL с pgvector)
        """
        # Проверяем, что используется PostgreSQL
        if "postgresql" not in settings.DATABASE_URL:
            logger.warning("Векторный поиск доступен только с PostgreSQL")
            return await self.get_all_facts()

        try:
            result = await self.db.execute(
                text("""
                    SELECT fact
                    FROM memories
                    WHERE character_id = :character_id
                    ORDER BY embedding <=> :query_embedding
                    LIMIT :limit
                """),
                {
                    "query_embedding": query_embedding,
                    "character_id": self.character_id,
                    "limit": limit
                }
            )
            return [row[0] for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Ошибка векторного поиска: {e}")
            return await self.get_all_facts()

    async def get_all_facts(self) -> list[str]:
        """Получить все факты"""
        result = await self.db.execute(
            text("SELECT fact FROM memories WHERE character_id = :character_id"),
            {"character_id": self.character_id}
        )
        return [row[0] for row in result.fetchall()]

    async def count_facts(self) -> int:
        """Количество фактов"""
        result = await self.db.execute(
            text("SELECT COUNT(*) FROM memories WHERE character_id = :character_id"),
            {"character_id": self.character_id}
        )
        return result.scalar()

    async def clear_all(self):
        """Удалить все факты"""
        await self.db.execute(
            text("DELETE FROM memories WHERE character_id = :character_id"),
            {"character_id": self.character_id}
        )
        await self.db.commit()
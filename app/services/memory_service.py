from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.memory import Memory
from app.services.ai_service import get_embedding
import logging

logger = logging.getLogger(__name__)


class MemoryService:
    def __init__(self, db: AsyncSession, character_id: int):
        self.db = db
        self.character_id = character_id

    async def add_fact(self, fact: str, embedding: list = None):
        """
        Сохранить факт с вектором

        Args:
            fact: Текст факта
            embedding: Вектор эмбеддинга (если None - будет сгенерирован автоматически)
        """
        # Если эмбеддинг не передан - генерируем
        if embedding is None:
            embedding = get_embedding(fact)
            logger.debug(f"Сгенерирован эмбеддинг для факта: {fact[:50]}...")

        memory = Memory(
            character_id=self.character_id,
            fact=fact,
            embedding=embedding if embedding else None
        )
        self.db.add(memory)
        await self.db.commit()
        logger.info(f"✅ Факт сохранен: {fact[:50]}...")

    async def get_relevant_facts(self, query: str, limit: int = 5) -> list[str]:
        """
        Векторный поиск фактов по смыслу

        Args:
            query: Текст запроса
            limit: Максимальное количество фактов

        Returns:
            list[str]: Список релевантных фактов
        """
        try:
            # Получаем эмбеддинг для запроса
            query_embedding = get_embedding(query)

            if not query_embedding or all(v == 0 for v in query_embedding):
                logger.warning("Не удалось получить эмбеддинг для запроса")
                return await self.get_all_facts()

            # Выполняем векторный поиск
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

            facts = [row[0] for row in result.fetchall()]
            logger.info(f"🔍 Найдено {len(facts)} релевантных фактов")
            return facts

        except Exception as e:
            logger.error(f"❌ Ошибка векторного поиска: {e}")
            # В случае ошибки возвращаем все факты
            return await self.get_all_facts()

    async def get_all_facts(self) -> list[str]:
        """Получить все факты пользователя"""
        try:
            result = await self.db.execute(
                text("SELECT fact FROM memories WHERE character_id = :character_id"),
                {"character_id": self.character_id}
            )
            facts = [row[0] for row in result.fetchall()]
            logger.info(f"📚 Получено {len(facts)} фактов")
            return facts
        except Exception as e:
            logger.error(f"❌ Ошибка получения фактов: {e}")
            return []

    async def count_facts(self) -> int:
        """Получить количество фактов"""
        try:
            result = await self.db.execute(
                text("SELECT COUNT(*) FROM memories WHERE character_id = :character_id"),
                {"character_id": self.character_id}
            )
            return result.scalar() or 0
        except Exception as e:
            logger.error(f"❌ Ошибка подсчета фактов: {e}")
            return 0

    async def clear_all(self):
        """Очистить все факты пользователя"""
        try:
            await self.db.execute(
                text("DELETE FROM memories WHERE character_id = :character_id"),
                {"character_id": self.character_id}
            )
            await self.db.commit()
            logger.info(f"🧹 Очищены все факты для character_id={self.character_id}")
        except Exception as e:
            logger.error(f"❌ Ошибка очистки фактов: {e}")
            await self.db.rollback()
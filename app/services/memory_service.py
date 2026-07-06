import chromadb
from chromadb.utils import embedding_functions
from app.config import settings
import uuid


# Инициализация клиента ChromaDB (хранилище в папке ./chroma_data)
chroma_client = chromadb.PersistentClient(path="./chroma_data")

# Используем embedding-функцию от OpenAI (можно заменить на любую другую)
# Но для работы с русским языком лучше использовать sentence-transformers
# Пока используем стандартную функцию, потом заменим на rubert
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"  # хорошая модель для русского
)


class MemoryService:
    def __init__(self, character_id: int):
        self.character_id = character_id
        # Коллекция для этого персонажа
        self.collection_name = f"character_{character_id}"

        # Создаём коллекцию, если её нет
        try:
            self.collection = chroma_client.get_collection(self.collection_name)
        except:
            self.collection = chroma_client.create_collection(
                name=self.collection_name,
                embedding_function=embedding_fn
            )

    async def add_fact(self, fact: str):
        """Сохранить факт в память персонажа"""
        # Генерируем уникальный ID
        fact_id = str(uuid.uuid4())

        self.collection.add(
            documents=[fact],
            ids=[fact_id],
            metadatas=[{"character_id": self.character_id, "fact": fact}]
        )
        print(f"🧠 Сохранён факт: {fact}")

    async def get_relevant_facts(self, query: str, limit: int = 5) -> list[str]:
        """Найти релевантные факты по запросу"""
        if self.collection.count() == 0:
            return []

        results = self.collection.query(
            query_texts=[query],
            n_results=min(limit, self.collection.count())
        )

        # Извлекаем только текст фактов
        if results and results['documents']:
            return [doc for doc in results['documents'][0] if doc]
        return []

    async def get_all_facts(self) -> list[str]:
        """Получить все сохранённые факты"""
        if self.collection.count() == 0:
            return []

        results = self.collection.get()
        return results['documents'] if results and 'documents' in results else []

    async def count_facts(self) -> int:
        """Количество сохранённых фактов"""
        return self.collection.count()

    async def clear_all(self):
        """Полностью удалить память персонажа"""
        try:
            # Удаляем коллекцию
            chroma_client.delete_collection(self.collection_name)
            print(f"🧹 Коллекция {self.collection_name} удалена")
        except Exception as e:
            print(f"⚠️ Коллекция не найдена: {e}")

        # Создаём новую пустую коллекцию
        self.collection = chroma_client.create_collection(
            name=self.collection_name,
            embedding_function=embedding_fn
        )
        print(f"✅ Новая коллекция {self.collection_name} создана")

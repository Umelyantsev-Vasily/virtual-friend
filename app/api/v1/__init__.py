from fastapi import APIRouter
from app.api.v1.characters import router as characters_router
from app.api.v1.chat import router as chat_router

# Создаем главный роутер для v1
router = APIRouter()

# Подключаем все под-роутеры
router.include_router(characters_router)
router.include_router(chat_router)

__all__ = ["router"]
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.character_service import CharacterService
from app.services.message_service import MessageService
from app.services.ai_service import generate_response
from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/send", response_model=MessageResponse)
async def send_message(
        message_data: MessageCreate,
        telegram_id: str,
        db: AsyncSession = Depends(get_db)
):
    char_service = CharacterService(db)
    msg_service = MessageService(db)

    # Получаем персонажа
    character = await char_service.get_by_user_id(telegram_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Сохраняем сообщение пользователя
    await msg_service.save_user_message(character.id, message_data.content)

    # Получаем историю для AI (последние 10 сообщений)
    history = await msg_service.get_history_for_ai(character.id, limit=10)

    # Генерируем ответ с учётом истории
    ai_reply = await generate_response(
        character_name=character.name,
        personality=character.personality,
        user_message=message_data.content,
        history=history
    )

    # Сохраняем ответ AI
    ai_message = await msg_service.save_assistant_message(character.id, ai_reply)
    return ai_message


@router.get("/history/{character_id}", response_model=list[MessageResponse])
async def get_history(
        character_id: int,
        telegram_id: str,
        limit: int = 50,
        db: AsyncSession = Depends(get_db)
):
    char_service = CharacterService(db)

    # Проверяем доступ
    character = await char_service.get_by_user_id(telegram_id)
    if not character or character.id != character_id:
        raise HTTPException(status_code=404, detail="Character not found")

    # Получаем историю
    msg_service = MessageService(db)
    messages = await msg_service.get_history(character_id, limit)
    return messages
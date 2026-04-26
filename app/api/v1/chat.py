from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.character import Character
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/send", response_model=MessageResponse)
async def send_message(
        message_data: MessageCreate,
        telegram_id: str,
        db: AsyncSession = Depends(get_db)
):
    # 1. Проверяем, что персонаж принадлежит пользователю
    result = await db.execute(
        select(Character).where(
            Character.id == message_data.character_id,
            Character.user_telegram_id == telegram_id
        )
    )
    character = result.scalar_one_or_none()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # 2. Сохраняем сообщение пользователя
    user_message = Message(
        character_id=message_data.character_id,
        role="user",
        content=message_data.content
    )
    db.add(user_message)
    await db.commit()
    await db.refresh(user_message)

    # Пока возвращаем просто сообщение (позже добавим OpenAI)
    return user_message


@router.get("/history/{character_id}", response_model=list[MessageResponse])
async def get_history(
        character_id: int,
        telegram_id: str,
        limit: int = 50,
        db: AsyncSession = Depends(get_db)
):
    # Проверяем доступ
    result = await db.execute(
        select(Character).where(
            Character.id == character_id,
            Character.user_telegram_id == telegram_id
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Character not found")

    # Получаем историю
    result = await db.execute(
        select(Message)
        .where(Message.character_id == character_id)
        .order_by(Message.created_at)
        .limit(limit)
    )
    return result.scalars().all()
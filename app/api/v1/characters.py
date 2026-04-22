from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterResponse
from typing import List


router = APIRouter(prefix="/characters", tags=["characters"])

@router.post("/", response_model=CharacterResponse)
async def create_character(
    character: CharacterCreate,
    telegram_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Создание нового персонажа"""
    new_character = Character(
        user_telegram_id=telegram_id,
        name=character.name,
        age=character.age,
        personality=character.personality,
        traits=character.traits,
        response_speed=character.response_speed,
        backstory=character.backstory,
        role=character.role
    )
    db.add(new_character)
    await db.commit()
    await db.refresh(new_character)
    return new_character

@router.get("/{telegram_id}", response_model=List[CharacterResponse])
async def get_characters(
    telegram_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Получить всех персонажей пользователя"""
    result = await db.execute(
        select(Character).where(Character.user_telegram_id == telegram_id)
    )
    characters = result.scalars().all()
    return characters

from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    user_telegram_id = Column(String(100), nullable=False, index=True)

    # Основные характеристики
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    personality = Column(Text, nullable=False)  # характер: "веселый, заботливый"
    traits = Column(JSON, default=list)  # черты: ["добрый", "романтичный"]
    response_speed = Column(String(30), default="thoughtful")  # instant, thoughtful, busy, absent
    backstory = Column(Text, nullable=True)  # предыстория персонажа
    role = Column(String(30), default="friend")  # friend, partner, father, mother

    # Состояние
    current_mood = Column(String(30), default="happy")

    # Системные поля
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

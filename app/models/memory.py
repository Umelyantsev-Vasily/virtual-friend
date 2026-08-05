from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, nullable=False)
    fact = Column(Text, nullable=False)
    embedding = Column(Vector(384))
    created_at = Column(DateTime, server_default=func.now())
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    character_id: int
    content: str


class MessageResponse(BaseModel):
    id: int
    character_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

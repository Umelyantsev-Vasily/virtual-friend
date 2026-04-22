from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CharacterCreate(BaseModel):
    name: str
    age: int
    personality: str
    traits: Optional[List[str]] = []
    response_speed: str = "thoughtful"
    backstory: Optional[str] = None
    role: str = "friend"


class CharacterResponse(BaseModel):
    id: int
    name: str
    age: int
    personality: str
    traits: List[str]
    response_speed: str
    backstory: Optional[str]
    role: str
    current_mood: str
    created_at: datetime

    class Config:
        from_attributes = True
        
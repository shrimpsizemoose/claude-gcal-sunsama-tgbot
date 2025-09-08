from pydantic import BaseModel
from datetime import datetime


class ChatMessage(BaseModel):
    timestamp: datetime
    role: str
    content: str


class UserState(BaseModel):
    user_id: str
    state: dict
    last_updated: datetime


class MockDataType(BaseModel):
    id: str
    name: str

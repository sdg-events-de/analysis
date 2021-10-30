from datetime import datetime
from typing import Optional
from .BaseModel import BaseModel


class LogResponse(BaseModel):
    id: int
    name: str
    levelno: Optional[int]
    levelname: Optional[str]
    created_at: datetime
    is_completed: bool

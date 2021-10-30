from typing import Optional
from .BaseModel import BaseModel


class EventResponse(BaseModel):
    id: int
    url: str
    host: Optional[str]
    display_title: Optional[str]
    status: str
    needs_review: bool

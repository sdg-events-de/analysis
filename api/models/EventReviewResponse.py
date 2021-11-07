from datetime import datetime
from typing import Optional
from .BaseModel import BaseModel


class EventResponse(BaseModel):
    id: int
    url: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    starts_at: Optional[datetime]
    ends_at: Optional[datetime]
    address: Optional[str]
    is_online: Optional[bool]
    status: Optional[str]
    status_note: Optional[str]


class EventReviewResponse(EventResponse):
    suggestion: EventResponse
    revision: EventResponse

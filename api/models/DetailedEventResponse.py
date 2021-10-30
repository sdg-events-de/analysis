from typing import Optional
from .BaseModel import BaseModel


class DetailedEventResponse(BaseModel):
    id: int
    url: str
    display_title: Optional[str]
    needs_review: bool
    attributes_to_review: Optional[list]

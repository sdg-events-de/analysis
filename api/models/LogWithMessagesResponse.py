from datetime import datetime
from .BaseModel import BaseModel
from .LogResponse import LogResponse


class LogMessageResponse(BaseModel):
    content: str
    logger: str
    levelno: int
    levelname: str
    created_at: datetime


class LogWithMessagesResponse(LogResponse):
    messages: list[LogMessageResponse]
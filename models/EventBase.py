import enum
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy_utils import ChoiceType
from . import BaseModel


class EventStatus(str, enum.Enum):
    published = "published"
    draft = "draft"
    deleted = "deleted"


# Serves as the foundation for both Event and EventVersion models
class EventBase(BaseModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    summary = Column(String)
    description = Column(String)
    starts_at = Column(TIMESTAMP(timezone=False))
    ends_at = Column(TIMESTAMP(timezone=False))
    address = Column(String)
    is_online = Column(Boolean)
    status = Column(ChoiceType(EventStatus))
    status_note = Column(String)

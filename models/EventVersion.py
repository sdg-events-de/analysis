import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .EventBase import EventBase
from .WithSuggestion import WithSuggestion


class VersionAction(enum.Enum):
    create = "create"
    discover = "discover"
    edit = "edit"
    review = "review"
    suggest = "suggest"


class EventVersion(EventBase, WithSuggestion):
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False, index=True)
    action = Column(Enum(VersionAction), nullable=False)

    event = relationship("Event", back_populates="versions", foreign_keys=event_id)

    def on_update(self):
        raise Exception("Event versions cannot be updated.")

    def on_delete(self):
        raise Exception("Event versions cannot be deleted.")
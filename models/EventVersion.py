import enum
from sqlalchemy import Column, Integer, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from .EventBase import EventBase
from helpers import hash_from_dict


class VersionAction(enum.Enum):
    create = "create"
    discover = "discover"
    edit = "edit"
    review = "review"
    suggest = "suggest"

    def __str__(self):
        return str(self.value)


class EventVersion(EventBase):
    event_id = Column(Integer, ForeignKey("event.id"), nullable=False, index=True)
    hash_id = Column(String, nullable=False)
    action = Column(Enum(VersionAction), nullable=False)

    event = relationship("Event", back_populates="versions", foreign_keys=event_id)

    # Generate a hash ID based on version attributes. The same attributes will
    # generate the same hash ID. So we can check if two versions are identical
    # by comparing their hash IDs.
    def generate_hash_id(self):
        self.hash_id = hash_from_dict(
            self.to_dict(
                exclude=[
                    "id",
                    "event_id",
                    "hash_id",
                    "action",
                    "created_at",
                    "updated_at",
                ]
            )
        )
        return self.hash_id

    def on_create(self):
        self.generate_hash_id()

    def on_update(self):
        raise Exception("Event versions cannot be updated.")

    def on_delete(self):
        raise Exception("Event versions cannot be deleted.")
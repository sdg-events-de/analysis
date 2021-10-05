from sqlalchemy.orm import relationship
from .EventBase import EventBase
from .EventVersion import EventVersion


class Event(EventBase):
    attributes = ["action"]

    versions = relationship(
        "EventVersion",
        back_populates="event",
        foreign_keys="EventVersion.event_id",
        order_by="desc(EventVersion.id)",
    )

    # Create a new event with status draft and action discover.
    # Used by the AI when it finds a new event via one of its pipelines.
    @classmethod
    def discover(cls, **kwargs):
        kwargs["status"] = kwargs.get("status", "draft")
        kwargs["action"] = kwargs.get("action", "discover")
        return cls.create(**kwargs)

    # Create an event versions snapshot based on current attributes
    def create_version(self, default_action):
        params = self.to_dict(exclude=["id", "created_at", "updated_at"])
        params["action"] = params["action"] or default_action
        for key in list(params):
            if key not in EventVersion.columns:
                del params[key]
        self.versions.append(EventVersion().fill(**params))

    # Mark the event as deleted (via status column)
    # Does not actually delete the event, just sets all fields to None and
    # sets status = deleted.
    def delete(self, status_note=None):
        # Set status to deleted
        self.status = "deleted"
        self.status_note = status_note or self.status_note

        # Reset all parameters to None
        params = self.to_dict(
            exclude=["id", "url", "status", "status_note", "created_at", "updated_at"]
        )
        for key in list(params):
            params[key] = None

        self.update(**params)

    # Create version on create
    def on_create(self):
        self.create_version(default_action="create")

    # Create version on update
    def on_update(self):
        self.create_version(default_action="edit")

    # Raise error on delete
    # Event records should not be deleted. Use .delete() instead to set
    # status = deleted.
    def on_delete(self):
        raise Exception(
            "Event cannot be deleted. Use the .delete() method to set the status to deleted."
        )

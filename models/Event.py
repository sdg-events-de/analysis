from sqlalchemy.orm import relationship
from .EventBase import EventBase
from .EventVersion import EventVersion


class Event(EventBase):
    action = None

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

    @property
    def versioned_attributes(self):
        return list(set(self.columns) - set(["id", "created_at", "updated_at"]))

    # Create an event versions snapshot based on current attributes
    def create_version(self, default_action=None):
        params = {}
        params["action"] = self.action or default_action
        for attribute in self.versioned_attributes:
            params[attribute] = getattr(self, attribute)
        self.versions.append(EventVersion().fill(**params))
        self.action = None

    def fill(self, **kwargs):
        self.action = kwargs.pop("action", self.action)
        return super().fill(**kwargs)

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
        if set(self.changed) & set(self.versioned_attributes):
            self.create_version(default_action="edit")

    # Raise error on delete
    # Event records should not be deleted. Use .delete() instead to set
    # status = deleted.
    def on_delete(self):
        raise Exception(
            "Event cannot be deleted. Use the .delete() method to set the status to deleted."
        )

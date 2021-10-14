from sqlalchemy import Column, String, Index, or_, and_
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from .EventBase import EventBase, EventStatus
from .WithSuggestion import WithSuggestion
from .EventVersion import EventVersion
from .EventSuggestion import EventSuggestion


class Event(EventBase, WithSuggestion):
    action = None

    # Make status and url non-nullable
    status = Column(ChoiceType(EventStatus), nullable=False)
    url = Column(String, nullable=False, index=True)

    # Add index to starts_at and ends_at
    __table_args__ = (
        Index("ix_event_starts_at", "starts_at"),
        Index("ix_event_ends_at", "ends_at"),
    )

    # Backpopulate suggestions
    suggestion = relationship(
        "EventSuggestion",
        back_populates="event",
        foreign_keys="Event.suggestion_id",
    )

    versions = relationship(
        "EventVersion",
        back_populates="event",
        foreign_keys="EventVersion.event_id",
        order_by="desc(EventVersion.id)",
    )

    @classmethod
    def filter_needing_review(cls):
        return cls.query.filter(
            or_(
                # Mismatching suggestion and revision
                cls.suggestion_id != cls.revision_id,
                # Has suggestion but no revision
                and_(cls.suggestion_id != None, cls.revision_id == None),
            )
        ).order_by(cls.id)

    # Create a new event with status draft and action discover.
    # Used by the AI when it finds a new event via one of its pipelines.
    @classmethod
    def discover(cls, url, **kwargs):
        # If event with this url already exists, do not do anything
        if cls.query.filter(cls.url == url).first():
            return

        # Create new event
        event = cls.create(url=url, status="draft", action="discover")

        # Create a suggestion from any additional parameters
        if kwargs:
            event.suggest(**kwargs)

        return event

    @property
    def versioned_attributes(self):
        return list(
            set(self.settable_attributes)
            - {"id", "created_at", "updated_at", "versions"}
        )

    @property
    def needs_review(self):
        return self.suggestion_id != self.revision_id

    # Return a list of attributes that need to be reviewed
    @property
    def attributes_to_review(self):
        return (self.suggestion or EventSuggestion(event=self)).attributes_to_review

    @property
    def display_title(self):
        return self.title or (self.suggestion or EventSuggestion(event=self)).title

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

    # Create new suggestion and save
    def suggest(self, **kwargs):
        suggestion = self.suggestion or EventSuggestion()
        suggestion.fill(**kwargs)

        if suggestion.changed:
            self.update(action="suggest", suggestion=suggestion.dup())

    def review(self, **kwargs):
        revision = self.suggestion.review(**kwargs)
        self.update(action="review", revision=revision, **kwargs)

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

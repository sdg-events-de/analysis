from furl import furl
from sqlalchemy import Column, String, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
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

    def __init__(self, **kwargs):
        self.suggestion = EventSuggestion()
        self.revision = self.suggestion
        super()

    @classmethod
    def find_by_url(cls, url):
        return cls.query.filter(cls.url == url).first()

    # Create a new event with status draft and action discover.
    # Used by the AI when it finds a new event via one of its pipelines.
    @classmethod
    def discover(cls, url, **kwargs):
        if cls.find_by_url(url):
            return False

        return cls.create(
            url=url,
            status="draft",
            action="discover",
            suggestion=EventSuggestion(url=url, **kwargs),
        )

    @property
    def versioned_attributes(self):
        return list(
            set(self.settable_attributes)
            - {"id", "created_at", "updated_at", "versions"}
        )

    @hybrid_property
    def needs_review(self):
        return self.suggestion_id != self.revision_id

    # Return a list of attributes that need to be reviewed
    @property
    def attributes_to_review(self):
        return self.suggestion.attributes_to_review

    @property
    def display_title(self):
        return self.title or self.suggestion.title

    @property
    def host(self):
        return furl(self.url).host

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
        new_suggestion = self.suggestion.dup().fill(**kwargs)

        if new_suggestion.is_identical(self.suggestion):
            return False

        self.update(action="suggest", suggestion=new_suggestion)
        return True

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
        params = {}
        exclude = {
            "id",
            "url",
            "suggestion_id",
            "revision_id",
            "status",
            "status_note",
            "created_at",
            "updated_at",
        }
        for key in set(self.columns) - exclude:
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

from sqlalchemy.orm import relationship
from sqlalchemy_mixins.utils import classproperty
from .EventBase import EventBase


class EventSuggestion(EventBase):
    event = relationship(
        "Event", foreign_keys="Event.suggestion_id", uselist=False, viewonly=True
    )

    # List of attributes that can be suggested
    @classproperty
    def suggestable_attributes(cls):
        return list(set(cls.columns) - {"id", "created_at", "updated_at"})

    # Return True if attribute has received a suggestion and suggested value
    # differs from last review.
    def attribute_needs_review(self, attribute):
        persisted_value = getattr(self.event, attribute)
        suggested_value = getattr(self, attribute)
        reviewed_value = getattr(self.revision or {}, attribute, None)

        return persisted_value != suggested_value and suggested_value != reviewed_value

    # Return a revision instance that represents a full or partial review of
    # this suggestion, depending on the provided kwargs. If kwargs cover all
    # attributes needing review, then the suggestion is returned (as the new
    # revision). Otherwise, a new revision object is returned that partially
    # copies attributes from this suggestion.
    def review(self, **kwargs):
        # Set up new revision and set reviewed attributes
        reviewed_attributes = set(kwargs) & set(self.attributes_to_review)
        revision = (self.revision or type(self)()).dup()
        for attr in reviewed_attributes:
            setattr(revision, attr, getattr(self, attr))

        # If suggestion and revision are the same, reuse suggestion as revision
        return self if self.is_equal(revision) else revision

    # Return a list of attributes that need to be reviewed
    @property
    def attributes_to_review(self):
        return list(
            filter(
                lambda x: self.attribute_needs_review(x),
                self.suggestable_attributes,
            )
        )

    @property
    def revision(self):
        return self.event.revision

    # Return True if two event suggestion instances are equal
    def is_equal(self, other):
        for attr in self.suggestable_attributes:
            if not getattr(self, attr) == getattr(other, attr):
                return False

        return True

    def on_update(self):
        raise Exception("Event suggestions cannot be updated.")

    def on_delete(self):
        raise Exception("Event suggestions cannot be deleted.")
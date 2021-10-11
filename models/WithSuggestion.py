from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import declared_attr, relationship

# Mixin to add suggestion and revision relationships to Event
class WithSuggestion:
    __abstract__ = True

    @declared_attr
    def suggestion_id(cls):
        return Column(Integer, ForeignKey("eventsuggestion.id"), nullable=True)

    @declared_attr
    def revision_id(cls):
        return Column(Integer, ForeignKey("eventsuggestion.id"), nullable=True)

    @declared_attr
    def suggestion(cls):
        return relationship("EventSuggestion", foreign_keys=cls.suggestion_id)

    @declared_attr
    def revision(cls):
        return relationship("EventSuggestion", foreign_keys=cls.revision_id)

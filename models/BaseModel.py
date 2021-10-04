from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy_mixins import AllFeaturesMixin, TimestampsMixin
from sqlalchemy_mixins.utils import classproperty

from helpers import get_database_session


Base = declarative_base()


class BaseModel(Base, AllFeaturesMixin, TimestampsMixin):
    __abstract__ = True
    attributes = []

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Overwrite the session property to get the current session or start a new
    # one. Sessions are created using contextvars, so they are local to each
    # thread.
    @classproperty
    def session(cls):
        return get_database_session()

    # Extend the constructor, so that custom attributes are also set
    def __init__(self, **kwargs):
        for attr in self.attributes:
            if attr in kwargs:
                setattr(self, attr, kwargs.pop(attr))
        super().__init__(**kwargs)

    # Extend settable_attributes, so that custom plain attributes are also set
    # by the .fill() method
    @classproperty
    def settable_attributes(cls):
        return super().settable_attributes + cls.attributes

    # Extend to_dict, so that custom plain attributes are also serialized
    def to_dict(self, **kwargs):
        dict = super().to_dict(**kwargs)

        # Add attributes
        for attr in self.attributes:
            if attr not in kwargs.get("exclude", []):
                dict[attr] = getattr(self, attr)

        return dict

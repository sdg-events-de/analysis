from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy_mixins import AllFeaturesMixin, TimestampsMixin
from sqlalchemy_mixins.utils import classproperty

from helpers import get_database_session


Base = declarative_base()


class BaseModel(Base, AllFeaturesMixin, TimestampsMixin):
    __abstract__ = True

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

    def on_create(self):
        pass

    def on_update(self):
        pass

    def on_delete(self):
        pass
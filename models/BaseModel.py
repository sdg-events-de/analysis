from sqlalchemy import MetaData, inspect
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy_mixins import AllFeaturesMixin, TimestampsMixin
from sqlalchemy_mixins.utils import classproperty

from helpers import get_database_session

# Declare naming convention for alembic to autogenerate names for indices,
# uniqueness constraints, foreign keys, etc...
# See: https://alembic.sqlalchemy.org/en/latest/naming.html
meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
Base = declarative_base(metadata=meta)


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

    # Return True if the given attribute has been modified
    def has_attribute_changed(self, attribute):
        history = getattr(inspect(self).attrs, attribute).history
        return bool(history.added) or bool(history.deleted)

    # Get all changed attributes
    # Mirrors ActiveRecord .changed property
    @property
    def changed(self):
        return filter(lambda x: self.has_attribute_changed(x), self.settable_attributes)

    def on_create(self):
        pass

    def on_update(self):
        pass

    def on_delete(self):
        pass
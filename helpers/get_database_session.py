import os
import contextvars
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.orm import sessionmaker, Session

# Using context var, we get a database session that is unique to the current
# thread
database_session = contextvars.ContextVar("database_session", default=None)
engine = create_engine(os.environ.get("DATABASE_URL"))
establish_session = sessionmaker(bind=engine, autocommit=True)


# Get the current database session or start a new one
def get_database_session():
    if database_session.get() == None:
        database_session.set(establish_session())

    return database_session.get()


# Listen for lifecycle events
def orm_lifecycle_events(session, _flush_context, _instances):
    for instance in session.new:
        if callable(getattr(instance, "on_create", None)):
            instance.on_create()

    for instance in session.dirty:
        if callable(getattr(instance, "on_update", None)):
            instance.on_update()

    for instance in session.deleted:
        if callable(getattr(instance, "on_delete", None)):
            instance.on_delete()


listen(Session, "before_flush", orm_lifecycle_events)
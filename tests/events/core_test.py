import re
import pytest
from models import Event, EventVersion


def test_it_can_create_event():
    event = Event.create(url="https://my-event.de", status="draft")

    # Sets status to draft
    assert event.status.value == "draft"

    # Creates event
    assert Event.query.count() == 1


def test_it_sets_status_deleted_on_delete():
    event = Event.create(url="test.com", status="draft", title="My title")
    event.delete()

    assert Event.query.count() == 1
    assert str(event.status) == "deleted"
    assert event.title == None
    assert event.url == "test.com"


def test_it_can_set_note_on_delete():
    event = Event.create(url="test.com", status="draft", title="My title")
    event.delete(status_note="Duplicate of 37")

    assert str(event.status) == "deleted"
    assert event.status_note == "Duplicate of 37"


def test_it_cannot_be_deleted():
    event = Event.create(url="https://my-event.de", status="draft")
    error = re.escape(
        "Event cannot be deleted. Use the .delete() method to set the status to deleted."
    )
    with pytest.raises(Exception, match=error):
        Event.session.delete(event)
        Event.session.flush()


def test_it_can_discover_events():
    event = Event.discover(url="https://google.com")

    # Sets status to draft
    assert event.status.value == "draft"

    # Sets event versions action to discover
    assert str(event.versions[0].action) == "discover"

    # Creates event and version
    assert Event.query.count() == 1
    assert EventVersion.query.with_parent(event).count() == 1

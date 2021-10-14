import re
import pytest
from models import Event


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
    assert event.status.value == "deleted"
    assert event.title == None
    assert event.url == "test.com"


def test_it_can_set_note_on_delete():
    event = Event.create(url="test.com", status="draft", title="My title")
    event.delete(status_note="Duplicate of 37")

    assert event.status.value == "deleted"
    assert event.status_note == "Duplicate of 37"


def test_it_cannot_be_deleted():
    event = Event.create(url="https://my-event.de", status="draft")
    error = re.escape(
        "Event cannot be deleted. Use the .delete() method to set the status to deleted."
    )
    with pytest.raises(Exception, match=error):
        Event.session.delete(event)
        Event.session.flush()


def test_it_correctly_identifies_enum_updates():
    event = Event.create(url="test", status="draft")

    # This should not treat event as changed
    event.fill(status="draft")
    assert event.changed == []

from datetime import datetime
from models import Event


def test_it_creates_a_version_on_create():
    event = Event.create(url="https://my-event.de", status="draft")

    # Creates event version
    assert len(event.versions) == 1

    # Version has the same attributes as event
    version = event.versions[0]
    assert version.url == "https://my-event.de"
    assert version.status.value == "draft"

    # Version action is create
    assert version.action.value == "create"


def test_it_creates_a_version_on_update():
    event = Event.create(url="https://my-event.de", status="draft")
    event.update(title="My Event", status="published")

    # Creates two event versions
    assert len(event.versions) == 2

    # Version has the same attributes as event
    version = event.versions[0]
    assert version.url == "https://my-event.de"
    assert version.status.value == "published"
    assert version.title == "My Event"

    # Version action is edit
    assert version.action.value == "edit"


def test_it_creates_a_version_on_delete():
    event = Event.create(
        url="https://my-event.de", status="draft", summary="My summary"
    )
    event.delete()

    # Creates two event versions
    assert len(event.versions) == 2

    # Version has attributes reset to null
    version = event.versions[0]
    assert version.url == "https://my-event.de"
    assert version.status.value == "deleted"
    assert version.summary == None

    # Version action is edit
    assert version.action.value == "edit"


def test_it_gets_all_versions_in_descending_order():
    event = Event.create(url="https://my-event.de", status="draft")
    event.update(title="My Event", status="published")

    # Creates two event versions
    assert len(event.versions) == 2

    # Edit is the latest version
    versions = event.versions
    assert versions[0].action.value == "edit"
    assert versions[1].action.value == "create"


def test_it_does_not_create_version_on_timestamp_change():
    event = Event.create(url="https://my-event.de", status="draft")
    updated_at = event.updated_at
    event.update(updated_at=datetime.now())

    assert updated_at != event.updated_at
    assert len(event.versions) == 1

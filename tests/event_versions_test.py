import pytest
from models import Event


def test_it_generates_consistent_hash_ids():
    event = Event.create(url="test", status="draft")
    version = event.versions[0]
    hash_id = version.hash_id

    assert version.generate_hash_id() == hash_id

    # These parameters should not affect hash ID
    version.event_id = 5
    version.id = 17
    version.hash_id = "testme"

    assert version.generate_hash_id() == hash_id

    # These parameters should affect hash ID
    version.status = "published"

    assert version.generate_hash_id() != hash_id


def test_it_cannot_update():
    event = Event.create(url="test", status="draft")
    version = event.versions[0]
    version.status = "published"
    with pytest.raises(Exception, match="Event versions cannot be updated."):
        version.save()


def test_it_cannot_delete():
    event = Event.create(url="test", status="draft")
    version = event.versions[0]
    with pytest.raises(Exception, match="Event versions cannot be deleted."):
        version.delete()
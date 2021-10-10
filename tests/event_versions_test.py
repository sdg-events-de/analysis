import pytest
from models import Event


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
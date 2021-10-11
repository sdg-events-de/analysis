import pytest
from models import EventSuggestion


def test_it_cannot_update():
    suggestion = EventSuggestion.create(status="draft")
    suggestion.status = "published"
    with pytest.raises(Exception, match="Event suggestions cannot be updated."):
        suggestion.save()


def test_it_cannot_delete():
    suggestion = EventSuggestion.create(url="test", status="draft")
    with pytest.raises(Exception, match="Event suggestions cannot be deleted."):
        suggestion.delete()
from models import Event


def test_it_can_create_event():
    event = Event.create(url="https://my-event.de", status="draft")

    # Sets status to draft
    assert event.status.value == "draft"

    # Creates event and version
    assert Event.query.count() == 1

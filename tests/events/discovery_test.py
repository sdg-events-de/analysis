from models import Event, EventVersion


def test_it_can_discover_events():
    event = Event.discover(url="example.com")

    # Sets status to draft
    assert event.status.value == "draft"

    # Sets event versions action to discover
    assert event.versions[0].action.value == "discover"

    # Creates no suggestion
    assert event.suggestion == None

    # Creates event and version
    assert Event.query.count() == 1
    assert EventVersion.query.with_parent(event).count() == 1


def test_it_can_discover_events_only_once():
    Event.discover(url="example.com")
    assert Event.query.count() == 1

    # Subsequent discoveries of the same URL do not create new events
    Event.discover(url="example.com")
    assert Event.query.count() == 1


def test_it_creates_suggestion_from_additional_params():
    event = Event.discover(url="example.com", summary="Lorem ipsum")

    # Creates event
    assert event.status.value == "draft"
    assert event.summary == None

    # Creates suggestion
    assert event.suggestion.summary == "Lorem ipsum"
    assert event.attributes_to_review == ["summary"]
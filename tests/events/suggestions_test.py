from models import Event


def test_it_can_suggest_changes():
    event = Event.create(url="https://google.com", status="draft")
    event.suggest(status="published", title="My title", summary="Lorem ipsum")

    # Does not modify event itself
    assert event.status.value == "draft"
    assert event.title == None
    assert event.summary == None

    # Creates a new suggestion for the event
    assert event.suggestion.status.value == "published"
    assert event.suggestion.title == "My title"
    assert event.suggestion.summary == "Lorem ipsum"

    # Tracks new suggestion in versioning
    assert len(event.versions) == 2
    assert event.versions[0].action.value == "suggest"
    assert event.versions[0].suggestion_id == event.suggestion_id


def test_it_can_suggest_more_changes():
    # Create a suggestion
    event = Event.create(url="test", status="draft")
    event.suggest(description="lorem ipsum")
    suggestion_id = event.suggestion_id
    assert suggestion_id != None

    # Create another suggestion
    event.suggest(summary="my summary")
    assert event.suggestion_id != suggestion_id
    assert event.suggestion.description == "lorem ipsum"
    assert event.suggestion.summary == "my summary"


def test_it_does_not_create_new_suggestion_when_equal_to_current_suggestion():
    event = Event.create(url="https://google.com", status="draft")
    event.suggest(status="published", title="My title", summary="Lorem ipsum")

    # Creates a new version with the suggestions
    assert len(event.versions) == 2
    suggestion_id = event.suggestion_id
    assert suggestion_id != None

    # Does not create a new identical suggestion
    assert (
        event.suggest(status="published", title="My title", summary="Lorem ipsum")
        == False
    )
    assert len(event.versions) == 2
    assert event.suggestion_id == suggestion_id


def test_it_identifies_attributes_to_review():
    event = Event.create(url="https://google.com", status="draft", description="abc")
    assert event.attributes_to_review == []

    event.suggest(
        status="published", title="My title", summary="Lorem ipsum", description="abc"
    )
    assert sorted(event.attributes_to_review) == sorted(["status", "title", "summary"])


def test_it_can_be_reviewed():
    event = Event.create(url="https://google.com", status="draft")
    assert event.suggest(status="published", title="My title", summary="Lorem ipsum")
    assert event.needs_review == True

    event.review(status="published", title="My reviewed title", summary=None)

    # It marks event as having been reviewed
    assert event.needs_review == False
    assert event.revision == event.suggestion
    assert event.attributes_to_review == []
    assert event.versions[0].action.value == "review"


def test_it_can_be_partially_reviewed():
    event = Event.create(url="https://google.com", status="draft")
    event.suggest(status="published", title="My title", summary="Lorem ipsum")
    assert event.needs_review == True

    event.review(status="published", title="My reviewed title")

    # Event continues needing review
    assert event.needs_review == True
    assert event.revision_id != event.suggestion_id
    assert event.attributes_to_review == ["summary"]
    assert event.versions[0].action.value == "review"


def test_it_can_get_all_events_needing_reviews():
    event1 = Event.create(url="https://google.com", status="draft")
    event1.suggest(status="published", title="My title", summary="Lorem ipsum")
    event1.review(status="published")

    event2 = Event.create(url="https://google.com", status="draft")
    event2.suggest(status="published", title="My title", summary="Lorem ipsum")

    Event.create(url="test", status="published")

    assert Event.query.filter(Event.needs_review).all() == [event1, event2]
from fastapi.testclient import TestClient
from tests.helpers import matches_dict
from api import api
from models import Event

client = TestClient(api)


class TestEventsIndex:
    def test_it_can_get_all_events(self):
        Event.create(url="testA", title="event A", status="draft")
        Event.create(url="testB", status="published").suggest(title="suggested title")
        response = client.get("/events")
        assert response.status_code == 200
        assert {
            "url": "testA",
            "display_title": "event A",
            "status": "draft",
            "needs_review": False,
        } == matches_dict(response.json()[0])
        assert {
            "url": "testB",
            "display_title": "suggested title",
            "status": "published",
            "needs_review": True,
        } == matches_dict(response.json()[1])


class TestEventsReview:
    def test_it_can_get_events_to_review(self):
        Event.create(url="testA", status="draft")
        Event.create(url="testB", status="published").suggest(title="suggested title")
        response = client.get("/events/review")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert {
            "url": "testB",
            "display_title": "suggested title",
            "status": "published",
            "needs_review": True,
        } == matches_dict(response.json()[0])

    def test_it_does_not_include_deleted_events(self):
        Event.create(url="example.com", status="deleted").suggest(title="abc")
        Event.create(url="example.com", status="deleted").suggest(status="published")
        response = client.get("/events/review")
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_it_only_includes_drafted_events_when_publication_is_suggested(self):
        Event.create(url="testA", status="draft").suggest(title="new title")
        Event.create(url="testB", status="draft").suggest(status="published")

        response = client.get("/events/review")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert {
            "url": "testB",
            "display_title": None,
            "status": "draft",
            "needs_review": True,
        } == matches_dict(response.json()[0])


class TestEventRead:
    def test_it_can_read_one_event(self):
        event = Event.create(url="example.com", status="draft")
        response = client.get(f"/events/{event.id}")
        assert response.status_code == 200
        assert {"url": "example.com"} == matches_dict(response.json())

    def test_it_responds_with_404_if_not_found(self):
        response = client.get("/events/1")
        assert response.status_code == 404
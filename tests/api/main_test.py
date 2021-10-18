from fastapi.testclient import TestClient
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
        }.items() <= response.json()[0].items()
        assert {
            "url": "testB",
            "display_title": "suggested title",
            "status": "published",
            "needs_review": True,
        }.items() <= response.json()[1].items()


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
        }.items() <= response.json()[0].items()


class TestEventRead:
    def test_it_can_read_one_event(self):
        event = Event.create(url="example.com", status="draft")
        response = client.get(f"/events/{event.id}")
        assert response.status_code == 200
        assert {"url": "example.com"}.items() <= response.json().items()

    def test_it_responds_with_404_if_not_found(self):
        response = client.get("/events/1")
        assert response.status_code == 404
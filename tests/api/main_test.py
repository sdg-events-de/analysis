from datetime import datetime
from fastapi.testclient import TestClient
from helpers import matches_dict
from api import api
from models import Event, Log, LogMessage

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


class TestEventsReviewPut:
    def test_it_can_submit_review(self):
        event = Event.create(url="testA", status="draft")
        event.suggest(title="new title")

        response = client.post(
            f"/events/review/{event.id}",
            json={"title": "reviewed title"},
        )
        assert response.status_code == 200
        assert {"success": True} == response.json()

        assert event.needs_review == False
        assert event.title == "reviewed title"

    def test_it_can_review_start_date(self):
        event = Event.create(url="testA", status="draft")

        client.post(
            f"/events/review/{event.id}",
            json={"starts_at": "2021-11-11T11:11:11"},
        )
        assert event.starts_at == datetime.fromisoformat("2021-11-11T11:11:11")

    def test_it_responds_with_404_if_event_does_not_exist(self):
        response = client.post(
            f"/events/review/3",
            json={"title": "some value"},
        )
        assert response.status_code == 404
        assert {"detail": "Event not found"} == response.json()

    def test_it_responds_with_422_if_invalid_field_is_reviewed(self):
        event = Event.create(url="testA", status="draft")
        event.suggest(title="new title")

        response = client.post(
            f"/events/review/{event.id}",
            json={"some_field": "some value"},
        )
        assert response.status_code == 422
        assert {"msg": "extra fields not permitted"} == matches_dict(
            response.json()["detail"][0]
        )


class TestEventRead:
    def test_it_can_read_one_event(self):
        event = Event.create(url="example.com", status="draft")
        response = client.get(f"/events/{event.id}")
        assert response.status_code == 200
        assert {"url": "example.com"} == matches_dict(response.json())

    def test_it_responds_with_404_if_not_found(self):
        response = client.get("/events/1")
        assert response.status_code == 404


class TestLogsIndex:
    def test_it_can_get_all_logs(self):
        log1 = Log.create(name="My scrape log", levelname="warn")
        log2 = Log.create(name="My second log")
        response = client.get("/logs")
        assert response.status_code == 200
        assert {
            "name": "My second log",
            "levelname": None,
            "created_at": log2.created_at.isoformat(),
            "is_completed": False,
        } == matches_dict(response.json()[0])
        assert {
            "name": "My scrape log",
            "levelname": "warn",
            "created_at": log1.created_at.isoformat(),
            "is_completed": False,
        } == matches_dict(response.json()[1])


class TestLogsRead:
    def test_it_can_read_all_messages(self):
        log = Log.create(name="My scrape log")
        msg1 = LogMessage.create(log=log, content="msg1", levelno=30, levelname="warn")
        msg2 = LogMessage.create(log=log, content="msg2", levelno=10, levelname="debug")
        log.complete()
        response = client.get(f"/logs/{log.id}")
        assert response.status_code == 200
        assert {
            "name": "My scrape log",
            "levelname": "warn",
            "levelno": 30,
            "created_at": log.created_at.isoformat(),
            "is_completed": True,
        } == matches_dict(response.json())
        assert {
            "content": "msg1",
            "levelname": "warn",
            "levelno": 30,
            "logger": "root",
            "created_at": msg1.created_at.isoformat(),
        } == matches_dict(response.json()["messages"][0])
        assert {
            "content": "msg2",
            "levelname": "debug",
            "levelno": 10,
            "logger": "root",
            "created_at": msg2.created_at.isoformat(),
        } == matches_dict(response.json()["messages"][1])

    def test_it_responds_with_404_if_not_found(self):
        response = client.get("/logs/1")
        assert response.status_code == 404

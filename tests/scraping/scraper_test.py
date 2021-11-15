from datetime import datetime, timedelta
from scrape.Scraper import Scraper
from models import Event


def test_it_scrapes_all_published_upcoming_events():
    event1 = Event.create(
        url="test",
        status="published",
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=2),
    )
    event2 = Event.create(
        url="test",
        status="published",
        starts_at=datetime.now() - timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=1),
    )

    assert Scraper.events_to_scrape() == [event1, event2]


def test_it_scrapes_any_unscraped_events():
    event1 = Event.create(
        url="test",
        status="draft",
    )
    event2 = Event.create(
        url="test",
        status="draft",
    )

    assert Scraper.events_to_scrape() == [event1, event2]


def test_it_does_not_scrape_published_expired_events():
    Event.create(
        url="test",
        status="published",
        ends_at=datetime.now() - timedelta(days=2),
    )

    assert len(Scraper.events_to_scrape()) == 0


def test_it_does_not_scrape_events_marked_for_deletion():
    Event.create(
        url="test",
        status="draft",
    ).suggest(status="deleted")

    assert len(Scraper.events_to_scrape()) == 0

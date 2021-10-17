from scrape.spiders.listings import spiders as listing_spiders
from scrape.spiders.events import spiders as event_spiders


def test_it_defines_2_listing_scrapers():
    assert len(listing_spiders) == 2


def test_it_defines_1_event_spider():
    assert len(event_spiders) == 1
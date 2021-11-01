import requests
import pytest
import scrapy
from scrapy.http import HtmlResponse
from scrape.spiders.listings.EngagementGlobalListingSpider import (
    EngagementGlobalListingSpider,
)
from helpers import matches_dict


@pytest.mark.vcr
def test_it_scrapes_events():
    url = EngagementGlobalListingSpider.start_urls[0]

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = list(EngagementGlobalListingSpider().parse(scrapy_response))

    events = [
        result for result in list(results) if not isinstance(result, scrapy.Request)
    ]
    assert len(events) == 10

    assert {
        "url": "https://skew.engagement-global.de/veranstaltung-detail/online-seminar-einstieg-in-den-kompass-nachhaltigkeit-3799.html",
        "title": "Online-Seminar Einstieg in den Kompass Nachhaltigkeit",
    } == matches_dict(events[0])

    assert {
        "url": "https://skew.engagement-global.de/veranstaltung-detail/fuenfter-runder-tisch-zu-kommunalen-partnerschaften-mit-china.html",
        "title": "5. Runder Tisch zu Kommunalen Partnerschaften mit China",
    } == matches_dict(events[1])


@pytest.mark.vcr
def test_it_returns_next_page():
    url = EngagementGlobalListingSpider.start_urls[0]

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = list(EngagementGlobalListingSpider().parse(scrapy_response))

    next_pages = [
        page.url for page in list(results) if isinstance(page, scrapy.Request)
    ]

    assert next_pages == [
        "https://www.engagement-global.de/veranstaltungssuche.html?page_e140=2#pgtop"
    ]

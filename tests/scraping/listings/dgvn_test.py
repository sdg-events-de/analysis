import requests
import pytest
from scrapy.http import HtmlResponse
from scrape.spiders.listings.DgvnListingSpider import DgvnListingSpider
from helpers import matches_dict


@pytest.mark.vcr
def test_it_scrapes_events():
    url = DgvnListingSpider.start_urls[0]

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = list(DgvnListingSpider().parse(scrapy_response))

    assert len(results) == 7

    assert {
        "url": "https://dgvn.de/aktivitaeten/einzelansicht/was-macht-eigentlich-der-igh/",
        "title": "Was macht eigentlich der IGH?",
    } == matches_dict(results[0])

    assert {
        "url": "https://dgvn.de/aktivitaeten/einzelansicht/fortschritte-herausforderungen-und-handlungsbedarf-koennen-wir-die-sdgs-mit-hilfe-der-wirtschaft-no/",
        "title": "Fortschritte, Herausforderungen und Handlungsbedarf: Können wir die SDGs mit Hilfe der Wirtschaft noch erreichen?",
    } == matches_dict(results[1])

    assert {
        "url": "https://dgvn.de/aktivitaeten/einzelansicht/gemeinsam-staerker-in-renningen/",
        "title": "Gemeinsam stärker in Renningen",
    } == matches_dict(results[2])

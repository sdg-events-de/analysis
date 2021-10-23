from datetime import datetime
import requests
import pytest
from freezegun import freeze_time
from scrapy.http import HtmlResponse
from scrape.spiders.events.DgvnEventSpider import DgvnEventSpider
from tests.helpers import matches_dict


@pytest.mark.vcr
def test_it_scrapes_event():
    url = "https://dgvn.de/aktivitaeten/einzelansicht/cop26-a-milestone-for-combatting-climate-change/"

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = DgvnEventSpider().parse(scrapy_response)
    event = next(results)

    assert {
        "url": url,
        "title": "COP26 - A milestone for Combatting Climate Change?",
        "summary": "The 26th UN Climate Change Conference (COP26) is crucial for reaching the goal of the Paris Agreement to limit global warming to well below 2, preferably to 1.5 degrees. The pressure to deliver is high.",
        "starts_at": datetime.fromisoformat("2021-11-12T11:30:00"),
        "ends_at": datetime.fromisoformat("2021-11-12T13:00:00"),
        "is_online": True,
        "address": None,
        "status": "deleted",
        "status_note": "Event does not mention SDGs",
    } == matches_dict(event)


@pytest.mark.vcr
def test_it_scrapes_multi_day_event():
    url = "https://dgvn.de/aktivitaeten/einzelansicht/treffen-ak-gendergerechtigkeit/"

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = DgvnEventSpider().parse(scrapy_response)
    event = next(results)

    assert {
        "url": url,
        "title": "Treffen AK Gendergerechtigkeit",
        "starts_at": datetime.fromisoformat("2021-11-19T19:00:00"),
        "ends_at": datetime.fromisoformat("2021-11-20T17:00:00"),
    } == matches_dict(event)


@pytest.mark.vcr
def test_it_scrapes_multi_day_event_across_two_months():
    url = "https://dgvn.de/aktivitaeten/einzelansicht/dieunundwir-3/"

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = DgvnEventSpider().parse(scrapy_response)
    event = next(results)

    assert {
        "url": url,
        "title": "#DieUNundWIR",
        "starts_at": datetime.fromisoformat("2020-02-17T12:00:00"),
        "ends_at": datetime.fromisoformat("2020-03-06T18:00:00"),
    } == matches_dict(event)


@pytest.mark.vcr()
@freeze_time("2021-09-11")
def test_it_marks_future_events_as_published():
    url = "https://dgvn.de/aktivitaeten/einzelansicht/sdg-seminar-oeko-soziale-gerechtigkeit-und-die-agenda-2030/"

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = DgvnEventSpider().parse(scrapy_response)
    event = next(results)

    assert {
        "url": url,
        "title": "SDG-Seminar: Öko-soziale Gerechtigkeit und die Agenda 2030",
        "starts_at": datetime.fromisoformat("2021-09-10T16:30:00"),
        "ends_at": datetime.fromisoformat("2021-09-12T14:00:00"),
        "status": "published",
        "status_note": None,
    } == matches_dict(event)


@pytest.mark.vcr
def test_it_marks_past_events_as_deleted():
    url = "https://dgvn.de/aktivitaeten/einzelansicht/sdg-seminar-oeko-soziale-gerechtigkeit-und-die-agenda-2030/"

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = DgvnEventSpider().parse(scrapy_response)
    event = next(results)

    assert {
        "url": url,
        "title": "SDG-Seminar: Öko-soziale Gerechtigkeit und die Agenda 2030",
        "starts_at": datetime.fromisoformat("2021-09-10T16:30:00"),
        "ends_at": datetime.fromisoformat("2021-09-12T14:00:00"),
        "status": "deleted",
        "status_note": "Event has ended",
    } == matches_dict(event)
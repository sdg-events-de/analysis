import requests
import pytest
from scrapy.http import HtmlResponse
from scrape.spiders.listings.Www17ZieleListingSpider import Www17ZieleListingSpider
from helpers import matches_dict


@pytest.mark.vcr()
def test_it_scrapes_events():
    url = Www17ZieleListingSpider.start_urls[0]

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = list(Www17ZieleListingSpider().parse(scrapy_response))

    assert len(results) == 20

    assert {
        "url": "https://culpeer-for-change.eu/",
        "title": "Culpeer4Change",
    } == matches_dict(results[0])

    assert {
        "url": "https://impacthub.de/events/climathon-2021/",
        "title": "Climathon Germany 2021",
    } == matches_dict(results[1])

    assert {
        "url": "https://veggienale.de/besuchen/frankfurt-2021",
        "title": "Veggienale & Fairgoods",
    } == matches_dict(results[2])

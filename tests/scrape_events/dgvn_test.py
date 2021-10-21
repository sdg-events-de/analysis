import requests
import pytest
from scrapy.http import HtmlResponse
from scrape.spiders.events.DgvnEventSpider import DgvnEventSpider


@pytest.mark.vcr
def test_it_scrapes_event():
    spider = DgvnEventSpider()
    url = "test.com"

    response = requests.get(
        "https://dgvn.de/aktivitaeten/einzelansicht/cop26-a-milestone-for-combatting-climate-change/"
    )

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=response.content, url=url)

    results = spider.parse(scrapy_response)
    event = next(results)

    assert {
        "title": "COP26 - A milestone for Combatting Climate Change?"
    }.items() <= event.items()
import scrapy
from scrape.items import EventItem
from scrape.pipelines import DiscoveryPipeline
from scrape.Parser import Parser


class EventListingBase(Parser):
    ATTRIBUTES = []

    def __iter__(self):
        return iter({key: getattr(self, key) for key in self.ATTRIBUTES}.items())

    def css(self, *args, **kwargs):
        return self.base_css.css(*args, **kwargs)


class ListingSpiderBase(scrapy.Spider):
    custom_settings = {
        "ITEM_PIPELINES": {
            DiscoveryPipeline: 100,
        }
    }
    EventListingClass = EventListingBase

    def events(self, response):
        return []

    def next_page(self, response):
        return None

    def parse(self, response):
        for event_css in self.events(response):
            yield EventItem(
                **dict(self.EventListingClass(response, base_css=event_css))
            )

        next_page = self.next_page(response)
        if next_page:
            yield from response.follow_all(next_page, callback=self.parse)

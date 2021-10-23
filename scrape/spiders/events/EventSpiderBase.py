from datetime import datetime
import scrapy
from scrape.items import EventItem
from scrape.pipelines import SuggestionPipeline
from scrape.helpers import Parser


class EventBase(Parser):
    ATTRIBUTES = []

    @property
    def url(self):
        return self.response.url

    def __iter__(self):
        return iter({key: getattr(self, key) for key in self.ATTRIBUTES}.items())

    def strptime(self, *args, **kwargs):
        return datetime.strptime(*args, **kwargs)

    def combine_date_and_time(self, *args, **kwargs):
        return datetime.combine(*args, **kwargs)

    def time_now(self):
        return datetime.now()

    def base_css(self):
        return self.response

    def css(self, *args, **kwargs):
        return self.base_css().css(*args, **kwargs)


class EventSpiderBase(scrapy.Spider):
    custom_settings = {
        "ITEM_PIPELINES": {
            SuggestionPipeline: 100,
        }
    }
    EventClass = EventBase

    def parse(self, response):
        yield EventItem(**dict(self.EventClass(response)))
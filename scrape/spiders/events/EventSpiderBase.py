import warnings
from datetime import datetime
import dateparser
import scrapy
from scrape.items import EventItem
from scrape.pipelines import SuggestionPipeline
from scrape.Parser import Parser

# Ignore dateparser warnings on PytzUsage
# See: https://github.com/scrapinghub/dateparser/issues/1013
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)


class EventBase(Parser):
    ATTRIBUTES = []

    @property
    def url(self):
        return self.response.url

    def __iter__(self):
        return iter({key: getattr(self, key) for key in self.ATTRIBUTES}.items())

    def parse_date(self, *args, **kwargs):
        return dateparser.parse(*args, **kwargs)

    def parse_time(self, *args, **kwargs):
        return dateparser.parse(*args, **kwargs)

    def combine_date_and_time(self, *args, **kwargs):
        return datetime.combine(*args, **kwargs)

    def time_now(self):
        return datetime.now()

    def time_midnight(self):
        return datetime.min.time()

    def css(self, *args, **kwargs):
        return self.base_css.css(*args, **kwargs)


class EventSpiderBase(scrapy.Spider):
    custom_settings = {
        "ITEM_PIPELINES": {
            SuggestionPipeline: 100,
        }
    }
    EventClass = EventBase

    def parse(self, response):
        yield EventItem(**dict(self.EventClass(response)))
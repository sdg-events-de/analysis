import scrapy
from scrape.items import EventItem
from scrape.pipelines import DiscoveryPipeline
from scrape.helpers.Parser import Parser


class EventListingSpiderBase(scrapy.Spider):
    custom_settings = {
        "ITEM_PIPELINES": {
            DiscoveryPipeline: 100,
        }
    }

    EVENT_TAG = None
    TITLE_TAG = None
    SUMMARY_TAG = None
    URL_TAG = None

    def extract_title(self, event):
        return event.extract_text(self.TITLE_TAG)

    def extract_summary(self, event):
        return event.extract_text(self.SUMMARY_TAG)

    def extract_url(self, event):
        return event.extract_href(self.URL_TAG)

    def parse(self, response):
        events = [Parser(event, response) for event in response.css(self.EVENT_TAG)]

        for event in events:
            yield EventItem(
                title=self.extract_title(event),
                # "date": extract_text_from(event, self.event_date_tag),
                summary=self.extract_summary(event),
                url=self.extract_url(event),
            )
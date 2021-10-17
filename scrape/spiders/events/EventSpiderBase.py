import scrapy
from scrape.items import EventItem
from scrape.pipelines import SuggestionPipeline
from scrape.helpers.Parser import Parser


class EventSpiderBase(scrapy.Spider):
    custom_settings = {
        "ITEM_PIPELINES": {
            SuggestionPipeline: 100,
        }
    }

    EVENT_TAG = None
    TITLE_TAG = None
    SUMMARY_TAG = None
    DESCRIPTION_TAG = None

    def extract_title(self, event):
        if self.TITLE_TAG is None:
            return None
        return event.extract_text(self.TITLE_TAG)

    def extract_summary(self, event):
        if self.SUMMARY_TAG is None:
            return None
        return event.extract_text(self.SUMMARY_TAG)

    def extract_description(self, event):
        if self.DESCRIPTION_TAG is None:
            return None
        return event.extract_text(self.DESCRIPTION_TAG)

    def parse(self, response):
        event = Parser(response.css(self.EVENT_TAG), response)

        yield EventItem(
            id=self.event_id,
            url=response.url,
            title=self.extract_title(event),
            # "date": extract_text_from(event, self.event_date_tag),
            summary=self.extract_summary(event),
            description=self.extract_description(event),
        )
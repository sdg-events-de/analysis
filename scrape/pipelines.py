from models import Event
from scrape.scrape_log import scrape_log


class DiscoveryPipeline:
    def process_item(self, item, spider):
        if Event.discover(**item):
            scrape_log.info(f"Event discovered: {item['url']}")
        return item


class SuggestionPipeline:
    def process_item(self, item, spider):
        event = Event.find(spider.event_id)
        if event.suggest(**item):
            scrape_log.info(f"Event #{event.id} updated: {event.url}")
        return item
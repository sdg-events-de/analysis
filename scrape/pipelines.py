import copy
from models import Event


class DiscoveryPipeline:
    def process_item(self, item, spider):
        Event.discover(**item)
        return item


class SuggestionPipeline:
    def process_item(self, item, spider):
        suggestion = copy.deepcopy(item)
        event = Event.find(spider.event_id)
        event.suggest(**suggestion)
        return item
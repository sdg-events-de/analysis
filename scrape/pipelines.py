from models import Event


class DiscoveryPipeline:
    def process_item(self, item, spider):
        Event.discover(**item)
        return item

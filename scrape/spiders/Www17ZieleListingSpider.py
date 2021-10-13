from scrape.helpers.EventListingSpiderBase import EventListingSpiderBase


class Www17ZieleListingSpider(EventListingSpiderBase):
    name = "www17ZieleListing"
    allowed_domains = ["17ziele.de"]
    start_urls = ["https://17ziele.de/events.html"]

    EVENT_TAG = ".event"
    TITLE_TAG = "h2"
    SUMMARY_TAG = ".ce_text.block"
    URL_TAG = "p.more"
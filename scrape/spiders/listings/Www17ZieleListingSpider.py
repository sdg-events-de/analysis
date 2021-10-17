from .ListingSpiderBase import ListingSpiderBase


class Www17ZieleListingSpider(ListingSpiderBase):
    name = "www17ZieleListing"
    allowed_domains = ["17ziele.de"]
    start_urls = ["https://17ziele.de/events.html"]

    EVENT_TAG = ".event"
    TITLE_TAG = "h2"
    SUMMARY_TAG = ".ce_text.block"
    URL_TAG = "p.more"
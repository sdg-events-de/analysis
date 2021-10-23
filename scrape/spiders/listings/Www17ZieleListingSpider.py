from .ListingSpiderBase import EventListingBase, ListingSpiderBase


class Www17ZieleEventListing(EventListingBase):
    ATTRIBUTES = ["url", "title"]

    @property
    def url(self):
        return self.extract_href("p.more")

    @property
    def title(self):
        return self.extract_text("h2")


class Www17ZieleListingSpider(ListingSpiderBase):
    name = "www17ZieleListing"
    allowed_domains = ["17ziele.de"]
    start_urls = ["https://17ziele.de/events.html"]
    EventListingClass = Www17ZieleEventListing

    def events(self, response):
        return response.css(".event")
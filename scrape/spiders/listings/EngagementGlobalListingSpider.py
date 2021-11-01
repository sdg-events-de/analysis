from .ListingSpiderBase import ListingSpiderBase, EventListingBase


class EngagementGlobalEventListing(EventListingBase):
    ATTRIBUTES = ["url", "title"]

    @property
    def title(self):
        return self.extract_text("h3")

    @property
    def url(self):
        return self.extract_href("a")


class EngagementGlobalListingSpider(ListingSpiderBase):
    name = "EngagementGlobalListing"
    allowed_domains = ["engagement-global.de"]
    start_urls = ["https://www.engagement-global.de/veranstaltungssuche.html"]
    EventListingClass = EngagementGlobalEventListing

    def next_page(self, response):
        return response.css("div.pagination a.next")

    def events(self, response):
        return response.css("div.event")
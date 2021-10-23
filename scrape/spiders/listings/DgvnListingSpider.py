from .ListingSpiderBase import ListingSpiderBase, EventListingBase


class DgvnEventListing(EventListingBase):
    ATTRIBUTES = ["url", "title"]

    @property
    def title(self):
        return self.extract_text("h4")

    @property
    def url(self):
        return self.extract_href("h4 a")


class DgvnListingSpider(ListingSpiderBase):
    name = "DgvnListing"
    allowed_domains = ["dgvn.de"]
    start_urls = ["https://dgvn.de/aktivitaeten/veranstaltungen/"]
    EventListingClass = DgvnEventListing

    def events(self, response):
        return response.css(".tx-event li")
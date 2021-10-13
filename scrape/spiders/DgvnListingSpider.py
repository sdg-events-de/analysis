from scrape.helpers.EventListingSpiderBase import EventListingSpiderBase


class DgvnListingSpider(EventListingSpiderBase):
    name = "DgvnListing"
    allowed_domains = ["dgvn.de"]
    start_urls = ["https://dgvn.de/aktivitaeten/veranstaltungen/"]

    EVENT_TAG = ".tx-event li"
    TITLE_TAG = "h4"
    SUMMARY_TAG = ".list__item-teaser"
    URL_TAG = "h4 a"

    def extract_summary(self, event):
        # Filter out "mehr" link at the end
        texts = filter(lambda x: x != "mehr", event.extract_text_list(self.SUMMARY_TAG))
        return event.join_texts(texts)
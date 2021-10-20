from .EventSpiderBase import EventSpiderBase


class DgvnEventSpider(EventSpiderBase):
    name = "DgvnEvent"
    allowed_domains = ["dgvn.de"]

    EVENT_TAG = "div.tx-event"
    # Keep only text directly within the h1 tag, ignore any subtags (like
    # subheader)
    TITLE_TAG = "h1.headline::text"
    SUMMARY_TAG = "div.detail__teaser"
    DESCRIPTION_TAG = "div.detail__content-body"
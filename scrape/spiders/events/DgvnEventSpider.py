from .EventSpiderBase import EventSpiderBase


class DgvnEventSpider(EventSpiderBase):
    name = "DgvnEvent"
    allowed_domains = ["dgvn.de"]

    EVENT_TAG = "div.tx-event"
    TITLE_TAG = "h1.headline"
    SUMMARY_TAG = "div.detail__teaser"
    DESCRIPTION_TAG = "div.detail__content-body"
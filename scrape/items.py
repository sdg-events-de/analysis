# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EventItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    description = scrapy.Field()
    starts_at = scrapy.Field()
    ends_at = scrapy.Field()
    address = scrapy.Field()
    is_online = scrapy.Field()
    status = scrapy.Field()
    status_note = scrapy.Field()

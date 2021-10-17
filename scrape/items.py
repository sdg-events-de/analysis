# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EventItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()

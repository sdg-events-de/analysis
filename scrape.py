from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrape.spiders import listing_spiders

process = CrawlerProcess(get_project_settings())

# Run all event listing spiders
for spider in listing_spiders:
    process.crawl(spider)

process.start()
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrape.spiders.listings import spiders as listing_spiders
from scrape.spiders.events import spiders as event_spiders
from models import Event


def scrape_listings():
    process = CrawlerProcess(get_project_settings())
    for spider in listing_spiders:
        process.crawl(spider)
    process.start()


def scrape_events():
    process = CrawlerProcess(get_project_settings())
    for event in Event.all():
        for spider in event_spiders:
            if event.host in spider.allowed_domains:
                process.crawl(spider, start_urls=[event.url], event_id=event.id)
    process.start()


p = Process(target=scrape_listings)
p.start()
p.join()

p = Process(target=scrape_events)
p.start()
p.join()

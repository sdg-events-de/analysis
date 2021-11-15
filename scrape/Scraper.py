from contextlib import contextmanager
from datetime import datetime
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess as ScrapyCrawlerProcess
from scrapy.utils.project import get_project_settings
from scrape.spiders.listings import spiders as listing_spiders
from scrape.spiders.events import spiders as event_spiders
from models import Event, EventSuggestion, Log
import logging


class LogFilter(logging.Filter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scrapy_log_level = getattr(logging, get_project_settings()["LOG_LEVEL"])

    def filter(self, record):
        is_scrapy_log = record.name.startswith("scrapy.") or record.name == "protego"

        if is_scrapy_log and record.levelno < self.scrapy_log_level:
            return 0

        return 1


# Wrapper class for Scrapy's CrawlerProcess
# Processes spiders sequentially rather than in parallel. This is slower but
# less error-prone.
class CrawlerProcess:
    process = None
    queue = []
    running = False

    def __init__(self, *args, **kwargs):
        self.process = ScrapyCrawlerProcess(*args, **kwargs)

    def crawl(self, *args, **kwargs):
        self.queue.append({"args": args, "kwargs": kwargs})

        if not (self.running):
            self.crawl_next()

    def crawl_next(self):
        if (len(self.queue)) == 0:
            self.running = False
            return

        self.running = True
        spider = self.queue.pop()
        deferred = self.process.crawl(*spider["args"], **spider["kwargs"])
        deferred.addCallback(lambda _: self.crawl_next())

    def join(self):
        self.process.join()

    def start(self):
        self.process.start()


class Scraper:
    log = None

    @staticmethod
    def scrape_listings_worker(log):
        Scraper.attach_logger(log)
        with Scraper.crawler_process() as process:
            for spider in listing_spiders:
                process.crawl(spider)

    @staticmethod
    def scrape_events_worker(log):
        Scraper.attach_logger(log)
        with Scraper.crawler_process() as process:
            for event in Scraper.events_to_scrape():
                for spider in event_spiders:
                    if event.host in spider.allowed_domains:
                        process.crawl(spider, start_urls=[event.url], event_id=event.id)

    # Get all events meeting one of two criteria:
    # 1. published & upcoming
    # 2. draft mode & not suggesting deletion
    @staticmethod
    def events_to_scrape():
        return (
            Event.query.join(Event.suggestion)
            .filter(
                ((Event.status == "published") & (Event.ends_at > datetime.now()))
                | ((Event.status == "draft") & (EventSuggestion.status == None))
                | ((Event.status == "draft") & (EventSuggestion.status != "deleted"))
            )
            .order_by("id")
            .all()
        )

    @staticmethod
    @contextmanager
    def crawler_process():
        process = CrawlerProcess(get_project_settings())

        try:
            yield process
        finally:
            process.join()
            process.start()

    @staticmethod
    def attach_logger(log):
        handler = log.create_handler()
        handler.addFilter(LogFilter())
        logging.root.addHandler(handler)

    @contextmanager
    def with_log(self):
        # Only the outermost with_log call should close the log
        should_close_log = False
        # Start new log if no log exists or previous log is done
        if self.log is None or self.log.is_completed:
            self.log = Log.create(name="Scraping")
            should_close_log = True

        try:
            yield self.log
        finally:
            if should_close_log:
                self.log.complete()

    def scrape(self):
        with self.with_log() as log:
            self.scrape_listings()
            self.scrape_events()

    def run_worker(self, *args, **kwargs):
        p = Process(*args, **kwargs)
        p.start()
        p.join()

    def scrape_listings(self):
        with self.with_log() as log:
            self.run_worker(target=Scraper.scrape_listings_worker, args=(log,))

    def scrape_events(self):
        with self.with_log() as log:
            self.run_worker(target=Scraper.scrape_events_worker, args=(log,))

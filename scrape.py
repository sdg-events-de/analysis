# from scrape.scrape_logger import ScrapeLogger
# from multiprocessing import Process, Queue
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from scrape.spiders.listings import spiders as listing_spiders
# from scrape.spiders.events import spiders as event_spiders
# from models import Event
# import logging
# from scrapy.logformatter import LogFormatter
# from io import StringIO
from scrape.Scraper import Scraper

runner = Scraper()
runner.scrape()
import logging
from scrapy.utils.project import get_project_settings

# Get log format settings from Scrapy
settings = get_project_settings()

# Log custom messages from spiders or pipelines
scrape_log = logging.getLogger("scrape_log")
scrape_log.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        settings["LOG_FORMAT"],
        settings["LOG_DATEFORMAT"],
    )
)
scrape_log.addHandler(handler)
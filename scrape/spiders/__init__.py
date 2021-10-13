import os
from pathlib import Path
import glob
import importlib

dirname = os.path.dirname(__file__)

listing_spider_files = glob.glob(os.path.join(dirname, "*ListingSpider.py"))
listing_spider_names = [Path(file).stem for file in listing_spider_files]

# List of event listing spiders
listing_spiders = [
    # Import each file and keep only the spider class
    getattr(importlib.import_module(f"scrape.spiders.{name}"), name)
    for name in listing_spider_names
]

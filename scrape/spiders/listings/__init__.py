import os
from pathlib import Path
import glob
import importlib

dirname = os.path.dirname(__file__)

spider_files = glob.glob(os.path.join(dirname, "*ListingSpider.py"))
spider_names = [Path(file).stem for file in spider_files]

# List of event listing spiders
spiders = [
    # Import each file and keep only the spider class
    getattr(importlib.import_module(f"scrape.spiders.listings.{name}"), name)
    for name in spider_names
]

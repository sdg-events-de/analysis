from scrape.spiders import listing_spiders


def test_it_defines_two_listing_scrapers():
    assert len(listing_spiders) == 2
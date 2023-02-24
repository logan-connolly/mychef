from pathlib import Path

import pytest

from scraper.spiders.full_helping_spider import UrlExtractor


@pytest.fixture
def recipe_index():
    yield (Path(__file__).parent / "webpages/full_helping.html").read_text()


@pytest.fixture(autouse=True)
def patch_full_helping_url(recipe_index, monkeypatch):
    monkeypatch.setattr(UrlExtractor, "get_start_page", lambda _: recipe_index)


def test_get_latest_recipe():
    extractor = UrlExtractor("http://thefullhelping.com")

    got = extractor.get_start_url()
    want = "https://www.thefullhelping.com/chai-spice-energy-balls/"

    assert got == want

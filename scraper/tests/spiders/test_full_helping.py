import pytest

from scraper.spiders.full_helping_spider import UrlExtractor


@pytest.mark.usefixtures("full_helping_homepage")
def test_get_latest_recipe(full_helping_homepage, monkeypatch):

    def mock_get_homepage(url):
        return full_helping_homepage

    monkeypatch.setattr(UrlExtractor, "get_homepage", mock_get_homepage)

    start_url = UrlExtractor("http://example.com").get_latest_recipe()
    expected_url = ["https://www.thefullhelping.com/chai-spice-energy-balls/"]
    assert start_url == expected_url

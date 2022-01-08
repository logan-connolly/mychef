import pytest

from scraper.spiders.full_helping_spider import UrlExtractor


@pytest.mark.usefixtures("full_helping_recipe_index")
def test_get_latest_recipe(full_helping_recipe_index, monkeypatch):
    def mock_get_start_page(url):
        return full_helping_recipe_index

    monkeypatch.setattr(UrlExtractor, "get_start_page", mock_get_start_page)

    start_url = UrlExtractor("http://thefullhelping.com").get_recipe_url()
    expected_url = ["https://www.thefullhelping.com/chai-spice-energy-balls/"]
    assert start_url == expected_url

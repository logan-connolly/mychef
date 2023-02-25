import functools
from typing import Iterable

import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.http.response.html import HtmlResponse

from .. import api, types


class FullHelpingSpider(scrapy.Spider):
    """Scrape the website thefullhelping.com and post results to mychef"""

    keyword = "thefullhelping"
    name = "full_helping"
    download_delay = 8

    def __init__(self, page: int = 1):
        self.url = f"https://www.thefullhelping.com/recipe-index/?sf_paged={page}"
        self.start_urls = [UrlExtractor(self.url).get_start_url()]

    def parse(self, response: HtmlResponse) -> Iterable[types.Recipe]:
        """Parse webpage to extract important recipe information"""
        if response.css(".wprm-recipe-ingredients-container"):
            payload: types.Recipe = {
                "url": response.url,
                "source_id": self.source_id,
                "image": self.get_image_url(response),
                "ingredients": self.get_ingredients(response),
                "name": response.css(".title::text").get("Unknown"),
            }
            yield payload

    @functools.cached_property
    def source_id(self) -> int:
        """Try and fetch source id from API, create it if it does not exist"""
        try:
            return api.get_source_id(query="thefullhelping")
        except ValueError:
            payload: types.Source = {
                "name": "TheFullHelping",
                "url": "http://thefullhelping.com",
            }
            return api.create_source_id(payload)

    @classmethod
    def get_image_url(cls, response: HtmlResponse) -> str:
        """Extract first image url that is nested under a figure tag"""
        image_figure, *_ = response.css("figure > img")
        return image_figure.re(r'src="(http.*?)\"')[0]

    @classmethod
    def get_ingredients(cls, response: HtmlResponse) -> str:
        """Get ingredients from specified html element"""
        selector = ".wprm-recipe-ingredients ::text"
        return " ".join(ingredient.get() for ingredient in response.css(selector))


class UrlExtractor:
    """Utility for extracting the start url for the TheFullHelping spider"""

    def __init__(self, url: str):
        self.url = url
        self.content = self.get_start_page()

    def get_start_page(self) -> bytes:
        """Get the start page for the spider"""
        try:
            return requests.get(self.url).content
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Unable to retrieve {self.url!r}") from None

    def get_start_url(self) -> str:
        """From start page find the starting url"""
        soup = BeautifulSoup(self.content, "html.parser")
        return soup.find("div", {"class": "single-posty"}).find("a")["href"]

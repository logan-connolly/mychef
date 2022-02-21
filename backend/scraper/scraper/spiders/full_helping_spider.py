from scraper.settings import API_URL
from typing import Union

import requests
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http.response.html import HtmlResponse

from ..util import UrlExtractor, create_source_id, get_source_id


class FullHelpingSpider(scrapy.Spider):
    """Scrape the website thefullhelping.com and post results to mychef"""

    keyword = "thefullhelping"
    name = "full_helping"
    download_delay = 8

    def __init__(self, page: int = 1):
        self.url = f"https://www.thefullhelping.com/recipe-index/?sf_paged={page}"
        self.start_urls = UrlExtractor(self.url).get_recipe_url()
        self.sid = self.retrieve_source_id()
        self.endpoint = f"{API_URL}/recipes/"

    def parse(self, response: HtmlResponse):
        """Parse webpage to extract important recipe information"""
        if response.css(".wprm-recipe-ingredients-container"):
            data = {
                "name": response.css(".title::text").get(),
                "source_id": self.sid,
                "url": response.url,
                "image": self.get_image_url(response),
                "ingredients": self.get_ingredients(response),
            }
            if all(val is not None for val in data.values()):
                resp = requests.post(self.endpoint, json=data)
                if resp.status_code == 400:
                    raise CloseSpider("Recipe already exists")

        for anchor_tag in response.css(".nav-previous a"):
            yield response.follow(anchor_tag, callback=self.parse)

    @classmethod
    def retrieve_source_id(cls):
        """Try and fetch source id, if does not exist, create it"""
        try:
            return get_source_id()
        except ValueError:
            payload = dict(name="TheFullHelping", url="http://thefullhelping.com")
            return create_source_id(payload)

    @classmethod
    def get_image_url(cls, response: HtmlResponse) -> Union[str, None]:
        """Extract image url from html response"""
        image_p = response.css("p > img")
        image_figure = response.css("figure > img")
        image_selectors = image_p if image_p else image_figure
        images_re = image_selectors.re(r'src="(http.*?)\"')
        images = [img for img in images_re if img.split(".")[-1] != "svg"]
        sorted_by_length = sorted(images, key=len, reverse=True)
        return sorted_by_length[0] if sorted_by_length else None

    @classmethod
    def get_ingredients(cls, response: HtmlResponse) -> Union[str, None]:
        """Get ingredients from specified html element"""
        ings = response.css(".wprm-recipe-ingredients ::text")
        return " ".join(ing.get() for ing in ings) if ings else None

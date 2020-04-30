import requests
import spacy
import scrapy

from scrapy.extensions.closespider import CloseSpider

from ..util import UrlExtractor, get_source_id


class FullHelpingSpider(scrapy.Spider):
    """Scrape the website thefullhelping.com and post results to mychef"""
    name = "full_helping"
    download_delay = 8

    def __init__(self, page=1):
        self.url = f"https://www.thefullhelping.com/recipe-index/?sf_paged={page}"
        self.start_urls = UrlExtractor(self.url).get_recipe_url()
        self.sid = get_source_id(domain="thefullhelping")

    def parse(self, response):
        if response.css(".wprm-recipe-ingredients-container"):
            payload = {
                "name": response.css(".title::text").get(),
                "url": response.url,
                "image": self.get_image_url(response),
            }
            if self.sid is None:
                raise CloseSpider("No source id found in database.")
            requests.post(f"http://api:8000/sources/{self.sid}/recipes/", json=payload)

        for a in response.css(".nav-previous a"):
            yield response.follow(a, callback=self.parse)

    def get_image_url(self, response):
        img = response.css("p > img")
        return img.re_first(r'src="(http.*?)\"')

    def get_ingredients(self, response):
        pass


class TrainData(scrapy.Spider):
    """Scrape the website thefullhelping.com and post results to mychef"""
    name = "train_data"
    download_delay = 8
    nlp = spacy.load("en_core_web_sm")

    def __init__(self, page=1):
        self.url = f"https://www.thefullhelping.com/recipe-index/?sf_paged={page}"
        self.start_urls = UrlExtractor(self.url).get_recipe_url()

    def parse(self, response):
        if response.css(".wprm-recipe-ingredients-container"):
            yield {
                "url": response.url,
                "ingredients": self.get_ingredients(response)
            }

        for a in response.css(".nav-previous a"):
            yield response.follow(a, callback=self.parse)

    def get_ingredients(self, response):
        ingredients_css = response.css(".wprm-recipe-ingredient-name::text")
        ingredients_raw = " ".join(ing.get() for ing in ingredients_css)
        doc = self.nlp(ingredients_raw)
        remove_punct = [tk.orth_ for tk in doc if not tk.is_punct | tk.is_space]
        return " ".join(word for word in remove_punct)

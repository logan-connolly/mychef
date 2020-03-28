import scrapy
import requests

from bs4 import BeautifulSoup


class UrlExtractor:
    """Utility for extracting the start url for the spider"""
    def __init__(self, url):
        self.url = url
        self.content = self.get_homepage()

    def get_homepage(self):
        try:
            return requests.get(self.url).content
        except requests.exceptions.ConnectionError as e:
            raise(e)

    def get_latest_recipe(self):
        soup = BeautifulSoup(self.content, "html.parser")
        latest_post = soup.find("div", {"class": "single-posty"})
        start_url = latest_post.find("a")["href"]
        return [start_url]


class FullHelpingSpider(scrapy.Spider):
    """Scrapes the website <thefullhelping.com> and posts to mychef"""
    name = "full_helping"
    url = "https://www.thefullhelping.com/recipe-index/"
    sid = 1
    download_delay = 8
    start_urls = UrlExtractor(url).get_latest_recipe()

    def parse(self, response):
        if response.css(".wprm-recipe-ingredients-container"):
            payload = {
                "name": response.css(".title::text").get(),
                "url": response.url,
                "image": self.get_image_url(response),
            }
            requests.post(f"http://api:8000/sources/{self.sid}/recipes/", json=payload)

        next_page_link = response.css(".nav-previous a::attr(href)").get()
        if next_page_link:
            next_page = response.urljoin(next_page_link)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def get_image_url(self, response):
        img = response.css("p > img")
        return img.re_first(r'src="(http.*?)\"')

    def get_ingredients(self, response):
        pass

import scrapy
import spacy
import string
import requests


class FullHelpingSpider(scrapy.Spider):
    """Scrapes the website <thefullhelping.com> for recipes"""

    name = "full_helping"
    sid = 1
    download_delay = 8

    start_urls = [
        "https://www.thefullhelping.com/recipe-index/",
    ]

    def parse(self, response):
        for post in response.css(".single-posty"):

            category = post.css('.cat div a::text').get()
            if not self.is_recipe(category):
                continue

            # Extract meta information from recipe index page
            payload = {
                "url": post.css("a::attr(href)").get(),
                "name": post.css(".title a::text").get(),
                "image": self.get_image_url(post),
            }
            requests.post(f"http://localhost:8002/sources/{self.sid}/recipes/", json=payload)

        next_page_link = response.css(".nav-previous a::attr(href)").get()
        if next_page_link:
            next_page = response.urljoin(next_page_link)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def get_image_url(self, post):
        attrs = ['style', 'data-bg']
        for attr in attrs:
            selection = post.css(f"#hero-image::attr({attr})").re(r'(http.*)\"')
            if selection:
                return selection[0]

    def is_recipe(self, category):
        cats = [
            "food and healing",
            "nutrition and wellness"
        ]
        return True if category.lower() not in cats else False


class FullHelpingRecipe(scrapy.Spider):
    """Scrape recipe for individual recipes"""

    name = "full_helping_recipe"
    sid = 1
    download_delay = 8
    nlp = spacy.load('en')

    def start_requests(self):
        urls = [
            "https://www.thefullhelping.com/creamy-cauliflower-turmeric-kale-soup/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ingredients_css = response.css(".wprm-recipe-ingredient-name::text")
        ingredients = " ".join(i.get() for i in ingredients_css)
        remove_punct = "".join(c for c in ingredients if c not in string.punctuation)
        doc = self.nlp(remove_punct)
        yield {"ingredients": [token for token in doc if token]}


import requests

from bs4 import BeautifulSoup


class UrlExtractor:
    """Utility for extracting the start url for the spider"""
    def __init__(self, url):
        self.url = url
        self.content = self.get_start_page()

    def get_start_page(self):
        try:
            return requests.get(self.url).content
        except requests.exceptions.ConnectionError as e:
            raise(e)

    def get_recipe_url(self):
        soup = BeautifulSoup(self.content, "html.parser")
        latest_post = soup.find("div", {"class": "single-posty"})
        start_url = latest_post.find("a")["href"]
        return [start_url]


def get_source_id(domain: str) -> int:
    resp = requests.get(f"http://api:8000/sources/?domain={domain}")
    if resp.ok:
        return resp.json()[0]["id"]

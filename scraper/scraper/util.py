import json
from typing import Dict

import requests
from bs4 import BeautifulSoup

from .settings import API_URL


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
    resp = requests.get(f"{API_URL}/sources/?domain={domain}")
    if resp.ok:
        return resp.json()[0]["id"]
    payload = dict(name="TheFullHelping", url="http://thefullhelping.com")
    return create_source_id(payload)


def create_source_id(payload: Dict[str, str]) -> int:
    resp = requests.post(f"{API_URL}/sources/", data=json.dumps(payload))
    return resp.json()["id"]

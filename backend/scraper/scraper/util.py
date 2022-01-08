import json
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from .settings import API_URL


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

    def get_recipe_url(self) -> List[str]:
        """From start page find the starting url"""
        soup = BeautifulSoup(self.content, "html.parser")
        latest_post = soup.find("div", {"class": "single-posty"})
        start_url = latest_post.find("a")["href"]
        return [start_url]


def get_source_id(domain: str) -> int:
    """Get the source id from API if exists, if not create it
    :param domain: Recipe url domain name (ie. 'thefullhelping')
    """
    url = f"{get_base_api_url()}/sources/?domain={domain}"
    try:
        resp = requests.get(url)
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Unable to retrieve {url!r}")

    if resp.ok:
        return resp.json()[0]["id"]
    raise ValueError("Domain could not be found")


def create_source_id(payload: Dict[str, str]) -> int:
    """Make post request to API to create TheFullHelping source"""
    url = f"{get_base_api_url()}/sources/"
    try:
        resp = requests.post(url, data=json.dumps(payload))
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Unable to retrieve {url!r}")

    if resp.ok:
        return resp.json()["id"]
    raise RuntimeError("Unable to create new source id")


def get_base_api_url() -> str:
    """Checks if environment variable is set and returns value"""
    if API_URL:
        return API_URL
    raise ValueError("Need to set INTERNAL_API_URL value")


def get_source_api_url(sid: int) -> str:
    """Formats url for fetching recipes from a given source id"""
    return f"{get_base_api_url()}/sources/{sid}/recipes/"

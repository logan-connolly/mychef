import json

import requests

from . import settings, types


def get_source_id(query: str) -> int:
    """Get the source id from API if exists"""
    try:
        resp = requests.get(settings.API_SOURCES_URL)
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Unable to retrieve {settings.API_SOURCES_URL!r}")

    if not resp.ok:
        raise ValueError("Response received, but with a bad status")

    try:
        return next(s["id"] for s in resp.json() if query in s["url"])
    except StopIteration as err:
        raise ValueError(f"Source id could not be found with {query!r}") from err


def create_source_id(payload: types.Source) -> int:
    """Make post request to API to create TheFullHelping source"""
    try:
        resp = requests.post(settings.API_SOURCES_URL, data=json.dumps(payload))
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Unable to retrieve {settings.API_SOURCES_URL!r}")

    if resp.ok:
        return resp.json()["id"]

    raise RuntimeError("Unable to create new source id")

import json

import pytest

from app.api.sources import CRUD


def test_read_source(test_app, monkeypatch):
    test_data = {"id": 1, "name": "Site Name", "url": "http://site.com"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(CRUD, "get", mock_get)

    response = test_app.get("/source/1")

    assert response.status_code == 200
    assert response.json() == test_data


def test_read_source_invalid(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(CRUD, "get", mock_get)

    response = test_app.get("/source/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Source not found"

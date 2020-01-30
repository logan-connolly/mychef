import json

import pytest

from app.api.sources import CRUD


def test_delete_source(test_app, monkeypatch):
    test_data = {"id": 1, "name": "New Name", "url": "http://newsite.com"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(CRUD, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(CRUD, "delete", mock_delete)

    response = test_app.delete("/source/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_delete_invalid_source_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(CRUD, "get", mock_get)

    response = test_app.delete("/source/1/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Source not found"

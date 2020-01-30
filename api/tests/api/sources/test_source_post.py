import json

import pytest

from app.api.sources import CRUD


def test_create_source(test_app, monkeypatch):
    test_request_payload = {"name": "Site Name", "url": "http://site.com"}
    test_response_payload = {"id": 1, "name": "Site Name", "url": "http://site.com"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(CRUD, "post", mock_post)

    response = test_app.post("/source/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_source_invalid(test_app):
    response = test_app.post("/source/", data=json.dumps({"name": "No URL"}))
    assert response.status_code == 422

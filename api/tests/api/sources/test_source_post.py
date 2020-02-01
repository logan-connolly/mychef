import json

import pytest

from app.api.sources import CRUD


def test_create_source(test_app, monkeypatch):
    test_request_payload = {"name": "Site Name", "url": "http://site.com"}
    test_response_payload = {"id": 1, "name": "Site Name", "url": "http://site.com"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(CRUD, "post", mock_post)

    response = test_app.post("/sources/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "payload, status_code",
    [
        [{"name": "No URL"}, 422],
        [{"name": "Bad URL", "url": "notaurl"}, 422],
    ]
)
def test_create_source_invalid(test_app, payload, status_code):
    response = test_app.post("/sources/", data=json.dumps(payload))
    assert response.status_code == status_code

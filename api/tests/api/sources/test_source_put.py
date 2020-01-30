import json

import pytest

from app.api.sources import CRUD


def test_update_source(test_app, monkeypatch):
    test_update_payload = {"id": 1, "name": "New Name", "url": "http://newsite.com"}

    async def mock_get(id):
        return True

    monkeypatch.setattr(CRUD, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(CRUD, "put", mock_put)

    response = test_app.put("/source/1/", data=json.dumps(test_update_payload),)
    assert response.status_code == 200
    assert response.json() == test_update_payload


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"name": "only name"}, 422],
        [1, {"url": "only url"}, 422],
        [999, {"name": "bad id", "url": "bad id"}, 404],
    ],
)
def test_update_source_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(CRUD, "get", mock_get)

    response = test_app.put(f"/source/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code

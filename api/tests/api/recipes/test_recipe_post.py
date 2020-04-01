import json

import pytest

from app.api import recipes


@pytest.mark.skip
def test_create_recipe(test_app, monkeypatch):
    test_request_payload = {
        "name": "Site Name",
        "url": "http://site.com",
        "image": "http://image.com",
    }
    test_response_payload = {
        "id": 1,
        "name": "Site Name",
        "url": "http://site.com",
        "image": "http://image.com",
        "sid": 1,
    }

    async def mock_post(sid, payload):
        return 1

    monkeypatch.setattr(recipes.CRUD, "post", mock_post)

    breakpoint()
    # todo: need to find out how to mock tests with nested endpoint
    response = test_app.post(
        "/sources/1/recipes/", data=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


@pytest.mark.skip
@pytest.mark.parametrize(
    "payload, status_code",
    [
        [{"name": "No URL"}, 422],
        [{"name": "Bad URL", "url": "notaurl", "image": "http://image.compile"}, 422],
        [
            {"name": "Bad Image Url", "url": "http://example.com", "image": "noturl"},
            422,
        ],
    ],
)
def test_create_recipe_invalid(test_app, payload, status_code):
    response = test_app.post("/sources/1/recipes/", data=json.dumps(payload))
    assert response.status_code == status_code

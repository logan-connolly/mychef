import json

import pytest

from app.core.config import settings

source = dict(name="Source", url="http://source.com")
sid: int = None
url: str = "http://url.com"
img: str = "http://img.com"


class TestRecipeInvalid:
    def test_create_source(self, client):
        global source
        global sid
        resp = client.post(f"{settings.api.version}/sources/", data=json.dumps(source))
        assert resp.status_code == 201
        sid = resp.json()["id"]
        source.update({"id": sid, "url": "source.com"})
        assert resp.json() == source

    @pytest.mark.parametrize(
        "recipe, code",
        [
            (dict(name="Not enough params"), 422),
            (dict(name="A", url="u", image=img, ingredients="egg"), 422),
            (dict(name="A", url=url, image="i", ingredients="egg"), 422),
            (dict(name="A", url=url, image=img, ingredients=["egg"]), 422),
        ],
    )
    def test_add_recipe_invalid(self, client, recipe, code):
        resp = client.post(
            f"{settings.api.version}/sources/1/recipes/", data=json.dumps(recipe)
        )
        assert resp.status_code == code

    def test_get_recipe_invalid(self, client):
        resp = client.get(f"{settings.api.version}/sources/{sid}/recipes/0/")
        assert resp.status_code == 404

    def test_get_recipes_invalid(self, client):
        resp = client.get(f"{settings.api.version}/sources/0/recipes/")
        assert resp.status_code == 404

    def test_update_recipe_invalid(self, client):
        resp = client.put(
            f"{settings.api.version}/sources/{sid}/recipes/0/", data=json.dumps(dict())
        )
        assert resp.status_code == 404

    def test_remove_recipe_invalid(self, client):
        resp = client.delete(f"{settings.api.version}/sources/{sid}/recipes/0/")
        assert resp.status_code == 404

    def test_remove_source(self, client):
        resp = client.delete(f"{settings.api.version}/sources/{sid}/")
        assert resp.status_code == 200

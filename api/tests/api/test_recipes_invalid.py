import json

import pytest

from app.core.config import settings

SOURCE = dict(name="Source", url="http://source.com")
SOURCE_ID = None
URL = "http://url.com"
IMG = "http://img.com"


class TestRecipeInvalid:
    def test_create_source(self, client):
        global SOURCE_ID
        resp = client.post(f"{settings.api.version}/sources/", data=json.dumps(SOURCE))
        assert resp.status_code == 201
        SOURCE_ID = resp.json()["id"]
        SOURCE.update({"id": SOURCE_ID, "url": "source.com"})
        assert resp.json() == SOURCE

    @pytest.mark.parametrize(
        "recipe, code",
        [
            (dict(name="Not enough params"), 422),
            (dict(name="A", url="u", image=IMG, ingredients="egg"), 422),
            (dict(name="A", url=URL, image="i", ingredients="egg"), 422),
            (dict(name="A", url=URL, image=IMG, ingredients=["egg"]), 422),
        ],
    )
    def test_add_recipe_invalid(self, client, recipe, code):
        resp = client.post(
            f"{settings.api.version}/sources/1/recipes/", data=json.dumps(recipe)
        )
        assert resp.status_code == code

    def test_get_recipe_invalid(self, client):
        resp = client.get(f"{settings.api.version}/sources/{SOURCE_ID}/recipes/0/")
        assert resp.status_code == 404

    def test_get_recipes_invalid(self, client):
        resp = client.get(f"{settings.api.version}/sources/0/recipes/")
        assert resp.status_code == 404

    def test_update_recipe_invalid(self, client):
        resp = client.put(
            f"{settings.api.version}/sources/{SOURCE_ID}/recipes/0/",
            data=json.dumps(dict()),
        )
        assert resp.status_code == 404

    def test_remove_recipe_invalid(self, client):
        resp = client.delete(f"{settings.api.version}/sources/{SOURCE_ID}/recipes/0/")
        assert resp.status_code == 404

    def test_remove_source(self, client):
        resp = client.delete(f"{settings.api.version}/sources/{SOURCE_ID}/")
        assert resp.status_code == 200

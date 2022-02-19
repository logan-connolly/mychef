import json

import pytest

from app.core.config import settings


class TestSourceInvalid:
    @pytest.mark.parametrize(
        "payload, code",
        [
            (dict(name="no url"), 422),
            (dict(name="bad url", url="url"), 422),
            (dict(name="no http", url="url.com"), 422),
        ],
    )
    def test_add_source_invalid(self, client, payload, code):
        data = json.dumps(payload)
        resp = client.post(f"{settings.api_version}/sources/", data=data)
        assert resp.status_code == code

    def test_get_source_invalid(self, client):
        resp = client.get(f"{settings.api_version}/sources/0/")
        assert resp.status_code == 404

    def test_get_sources_invalid(self, client):
        resp = client.get(f"{settings.api_version}/source/")
        assert resp.status_code == 404

    def test_update_source_invalid(self, client):
        resp = client.put(f"{settings.api_version}/sources/0/", data=json.dumps(dict()))
        assert resp.status_code == 404

    def test_remove_source_invalid(self, client):
        resp = client.delete(f"{settings.api_version}/sources/0/")
        assert resp.status_code == 404

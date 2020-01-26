import pytest
import falcon

from falcon import testing

from mychef_scraper.app import api


class TestSources:
    @pytest.fixture(scope="class")
    def client(self):
        yield testing.TestClient(api)

    def test_list_sources(self, client):
        doc = client.simulate_get('/sources')
        assert doc.status == falcon.HTTP_OK

    def test_get_source(self, client):
        resp = client.simulate_get(f'/source/{1}')
        assert resp.status == falcon.HTTP_OK

    def test_get_source_not_found(self, client):
        resp = client.simulate_get(f'/source/{-1}')
        assert resp.status == falcon.HTTP_404

import pytest

import falcon
from falcon import testing

from mychef_scraper.app import api


@pytest.fixture
def client():
    return testing.TestClient(api)


def test_list_sources(client):
    doc = {
        'sources': [
            {
                'name': 'The Full Helping',
                'url': 'https://www.thefullhelping.com/recipes/'
            }
        ]
    }

    response = client.simulate_get('/sources')
    result_doc = response.content

    assert result_doc == doc
    assert response.status == falcon.HTTP_OK

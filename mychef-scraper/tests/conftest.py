import pytest


@pytest.fixture
def doc():
    return {
        'sources': [
            {
                'id': 1,
                'name': 'The Full Helping',
                'url': 'https://www.thefullhelping.com/recipes/'
            }
        ]
    }

from pathlib import Path

import pytest


@pytest.fixture
def full_helping_recipe_index():
    fname = "webpages/full_helping.html"
    fpath = Path(__file__).parent.joinpath(fname)
    with open(fpath) as f:
        yield f.read()

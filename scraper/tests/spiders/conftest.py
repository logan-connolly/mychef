from pathlib import Path

import pytest


@pytest.fixture
def full_helping_homepage():
    fname = "webpages/full_helping.html"
    fpath = Path(__file__).parent.joinpath(fname)
    with open(fpath) as f:
        yield f.read()

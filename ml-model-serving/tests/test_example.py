import platform

import pytest


def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4


# https://docs.pytest.org/en/stable/explanation/fixtures.html
@pytest.fixture(params=[1, 2, 3], ids=["one", "two", "three"])
def ints(request):
    return request.param


# autouse
@pytest.fixture(params=["Linux", "Darwin", "Windows"], autouse=True)
def platform_system(request, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda _: request.param)


# to use fixture param ints
def test_on_ints(ints):
    assert ints**2 == ints * ints

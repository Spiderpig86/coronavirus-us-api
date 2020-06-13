"""Source Test

Source unit test.
"""


import pytest

from backend.models.classes.source import Source

EXPECTED_SOURCES = ["nyt", "jhu"]


def test__source__list__success():
    assert Source.list() == EXPECTED_SOURCES

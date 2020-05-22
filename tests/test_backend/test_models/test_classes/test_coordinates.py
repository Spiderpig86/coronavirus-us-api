"""Coordinates Test

Coordinates unit test.
"""


import pytest

from backend.models.classes.coordinates import Coordinates


@pytest.mark.parametrize(
    "latitude, longitude", [(1, 2), (-100, 1000000), ("5", 6), ("-41.123", "33.456")]
)
def test__coordinates__to_dict__success(latitude, longitude):
    coordinates = Coordinates(latitude, longitude)

    expected_response = {"latitude": latitude, "longitude": longitude}

    assert coordinates.to_dict() == expected_response

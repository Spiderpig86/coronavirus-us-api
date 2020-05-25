"""Location Properties Test

Location Properties unit test.
"""
import pytest

from backend.models.classes.coordinates import Coordinates
from backend.models.classes.location_properties import LocationProperties

VALID_LOCATION_PROPERTIES = LocationProperties(
    UID="uid",
    iso2="iso2",
    iso3="iso3",
    code3="code3",
    fips="fips",
    admin2="admin2",
    state="state",
    country="country",
    coordinates=Coordinates(40, 73),
    combined_key="combined_key",
    population=6000,
)


def test__vaLid_location_properties__to_dict__success():
    expected_dict = {
        "UID": "uid",
        "iso2": "iso2",
        "iso3": "iso3",
        "code3": "code3",
        "fips": "fips",
        "county": "admin2",
        "state": "state",
        "country": "country",
        "coordinates": Coordinates(40, 73).to_dict(),
        "combined_key": "combined_key",
        "population": 6000,
    }

    assert VALID_LOCATION_PROPERTIES.to_dict() == expected_dict


def test__build_coordinates__success():
    actual_coordinates = LocationProperties.build_coordinates(40, 73)
    expected_coordinates = Coordinates(40, 73)

    assert actual_coordinates.latitude == expected_coordinates.latitude
    assert actual_coordinates.longitude == expected_coordinates.longitude

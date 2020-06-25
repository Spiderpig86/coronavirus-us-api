"""Location Test

Location unit test.
"""
import pytest

from backend.models.classes.category import Category
from backend.models.classes.location import JhuLocation, Location, NytLocation
from backend.models.classes.location_properties import LocationProperties
from backend.models.classes.statistics import Statistics
from backend.utils.functions import Functions
from tests.base_test import TestBase


def test__given_valid_location__country_population__success():
    location = Location(**TestBase.VALID_LOCATION)
    assert location.country_population == TestBase.US_POPULATION


def test__given_valid_location__set_properties__success():
    location = Location(**TestBase.VALID_LOCATION)
    location_properties = LocationProperties(uid="123")
    location.set_properties(location_properties)

    assert location.properties.uid == "123"


def test__given_valid_location__to_dict__success():
    location = Location(**TestBase.VALID_LOCATION)

    assert location.to_dict() == {
        "id": TestBase.VALID_LOCATION["id"],
        "country": TestBase.VALID_LOCATION["country"],
        "last_updated": TestBase.VALID_LOCATION["last_updated"],
        "latest": TestBase.VALID_LOCATION["latest"],
    }

    assert location.to_dict(True) == {
        "id": TestBase.VALID_LOCATION["id"],
        "country": TestBase.VALID_LOCATION["country"],
        "last_updated": TestBase.VALID_LOCATION["last_updated"],
        "latest": TestBase.VALID_LOCATION["latest"],
        "timelines": {
            "confirmed": Category({"03-24-20": 5}).to_dict(),
            "deaths": Category({"03-24-20": 1}).to_dict(),
        },
    }

    assert location.to_dict(True, True) == {
        "id": TestBase.VALID_LOCATION["id"],
        "country": TestBase.VALID_LOCATION["country"],
        "last_updated": TestBase.VALID_LOCATION["last_updated"],
        "latest": TestBase.VALID_LOCATION["latest"],
        "timelines": {
            "confirmed": Category({"03-24-20": 5}).to_dict(),
            "deaths": Category({"03-24-20": 1}).to_dict(),
        },
        "properties": None,
    }


def test__given_jhu_location__to_dict__success():
    location = JhuLocation(**TestBase.VALID_JHU_LOCATION)

    assert location.to_dict() == {
        "id": TestBase.VALID_JHU_LOCATION["id"],
        "country": TestBase.VALID_JHU_LOCATION["country"],
        "last_updated": TestBase.VALID_JHU_LOCATION["last_updated"],
        "latest": TestBase.VALID_JHU_LOCATION["latest"],
        "uid": TestBase.VALID_JHU_LOCATION["uid"],
        "iso2": TestBase.VALID_JHU_LOCATION["iso2"],
        "iso3": TestBase.VALID_JHU_LOCATION["iso3"],
        "code3": TestBase.VALID_JHU_LOCATION["code3"],
        "state": TestBase.VALID_JHU_LOCATION["state"],
        "county": TestBase.VALID_JHU_LOCATION["county"],
        "fips": TestBase.VALID_JHU_LOCATION["fips"],
        "latitude": TestBase.VALID_JHU_LOCATION["latitude"],
        "longitude": TestBase.VALID_JHU_LOCATION["longitude"],
    }


def test__given_nyt_location__to_dict__success():
    location = NytLocation(**TestBase.VALID_NYT_LOCATION)

    assert location.to_dict() == {
        "id": TestBase.VALID_NYT_LOCATION["id"],
        "country": TestBase.VALID_NYT_LOCATION["country"],
        "last_updated": TestBase.VALID_NYT_LOCATION["last_updated"],
        "latest": TestBase.VALID_NYT_LOCATION["latest"],
        "state": TestBase.VALID_NYT_LOCATION["state"],
        "county": TestBase.VALID_NYT_LOCATION["county"],
        "fips": TestBase.VALID_NYT_LOCATION["fips"],
    }


@pytest.mark.parametrize(
    "a, b",
    [
        (Location(**TestBase.VALID_LOCATION), Location(**TestBase.VALID_LOCATION)),
        (
            JhuLocation(**TestBase.VALID_JHU_LOCATION),
            JhuLocation(**TestBase.VALID_JHU_LOCATION),
        ),
        (
            NytLocation(**TestBase.VALID_NYT_LOCATION),
            NytLocation(**TestBase.VALID_NYT_LOCATION),
        ),
    ],
)
def test__given_equal_locations__eq__sucess(a, b):
    assert a == b


def test__given_different_locations__eq__success():
    location_a = JhuLocation(**TestBase.VALID_JHU_LOCATION)
    location_b = JhuLocation(**TestBase.VALID_JHU_LOCATION)
    location_b.country = "CAN"

    assert location_a != location_b

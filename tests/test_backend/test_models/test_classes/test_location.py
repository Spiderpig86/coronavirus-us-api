"""Location Test

Location unit test.
"""
from backend.models.classes.category import Category
from backend.models.classes.location import JhuLocation, Location, NytLocation
from backend.models.classes.location_properties import LocationProperties
from backend.models.classes.statistics import Statistics
from backend.utils.functions import Functions

VALID_LOCATION = {
    "id": "id",
    "country": "US",
    "timelines": {
        "confirmed": Category({"03-24-20": 5}),
        "deaths": Category({"03-24-20": 1}),
    },
    "last_updated": Functions.get_formatted_date(),
    "latest": Statistics(50, 60),
}

VALID_NYT_LOCATION = {
    **VALID_LOCATION,
    "state": "state",
    "county": "county",
    "fips": "fips",
}

VALID_JHU_LOCATION = {
    **VALID_LOCATION,
    "uid": "uid",
    "iso2": "iso2",
    "iso3": "iso3",
    "code3": "code3",
    "state": "state",
    "county": "county",
    "fips": "fips",
    "latitude": "latitude",
    "longitude": "longitude",
}


US_POPULATION = 329466283


def test__given_valid_location__country_population__success():
    location = Location(**VALID_LOCATION)
    assert location.country_population == US_POPULATION


def test__given_valid_location__set_properties__success():
    location = Location(**VALID_LOCATION)
    location_properties = LocationProperties(UID="123")
    location.set_properties(location_properties)

    assert location.properties.UID == "123"


def test__given_valid_location__to_dict__success():
    location = Location(**VALID_LOCATION)

    assert location.to_dict() == {
        "id": VALID_LOCATION["id"],
        "country": VALID_LOCATION["country"],
        "last_updated": VALID_LOCATION["last_updated"],
        "latest": VALID_LOCATION["latest"],
    }

    assert location.to_dict(True) == {
        "id": VALID_LOCATION["id"],
        "country": VALID_LOCATION["country"],
        "last_updated": VALID_LOCATION["last_updated"],
        "latest": VALID_LOCATION["latest"],
        "timelines": {
            "confirmed": Category({"03-24-20": 5}).to_dict(),
            "deaths": Category({"03-24-20": 1}).to_dict(),
        },
    }

    assert location.to_dict(True, True) == {
        "id": VALID_LOCATION["id"],
        "country": VALID_LOCATION["country"],
        "last_updated": VALID_LOCATION["last_updated"],
        "latest": VALID_LOCATION["latest"],
        "timelines": {
            "confirmed": Category({"03-24-20": 5}).to_dict(),
            "deaths": Category({"03-24-20": 1}).to_dict(),
        },
        "properties": None,
    }


def test__given_jhu_location__to_dict__success():
    location = JhuLocation(**VALID_JHU_LOCATION)

    assert location.to_dict() == {
        "id": VALID_JHU_LOCATION["id"],
        "country": VALID_JHU_LOCATION["country"],
        "last_updated": VALID_JHU_LOCATION["last_updated"],
        "latest": VALID_JHU_LOCATION["latest"],
        "uid": VALID_JHU_LOCATION["uid"],
        "iso2": VALID_JHU_LOCATION["iso2"],
        "iso3": VALID_JHU_LOCATION["iso3"],
        "code3": VALID_JHU_LOCATION["code3"],
        "state": VALID_JHU_LOCATION["state"],
        "county": VALID_JHU_LOCATION["county"],
        "fips": VALID_JHU_LOCATION["fips"],
        "latitude": VALID_JHU_LOCATION["latitude"],
        "longitude": VALID_JHU_LOCATION["longitude"],
    }


def test__given_nyt_location__to_dict__success():
    location = NytLocation(**VALID_NYT_LOCATION)

    assert location.to_dict() == {
        "id": VALID_NYT_LOCATION["id"],
        "country": VALID_NYT_LOCATION["country"],
        "last_updated": VALID_NYT_LOCATION["last_updated"],
        "latest": VALID_NYT_LOCATION["latest"],
        "state": VALID_NYT_LOCATION["state"],
        "county": VALID_NYT_LOCATION["county"],
        "fips": VALID_NYT_LOCATION["fips"],
    }

"""Test Base

Class to hold main test utility functions.
"""
import json
from unittest import mock

from backend.models.classes.category import Category
from backend.models.classes.location import JhuLocation, NytLocation
from backend.models.classes.statistics import Statistics
from backend.utils.functions import Functions


class TestBase:

    TEST_DATE = "2020-05-30"

    SERVICE_LOCATION_FIELDS = ["id", "country", "timelines", "last_updated", "latest"]

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
        "timelines": {},  # This is allowed since we do not use this for more in depth testing
    }

    US_POPULATION = 329466283

    @staticmethod
    def _validate_json_from_file(serializable: object, actual_json_path: str):
        actual = json.dumps(serializable)

        with open(actual_json_path, "r") as f:
            expected = f.read()

        return json.loads(actual) == json.loads(expected)

    @staticmethod
    def _validate_json_from_file_str(actual: str, actual_json_path: str):
        with open(actual_json_path, "r") as f:
            expected = f.read()

        print()
        print(json.loads(expected))
        return actual == json.loads(expected)

    @staticmethod
    def _validate_fields(fields, dict):
        for field in fields:
            assert dict[field] is not None

    @staticmethod
    def _initialize_from_json(path, initializer):
        with open(path, "r") as f:
            data = f.read()

        json_data = json.loads(data)

        results = []
        for entry in json_data:
            confirmed = Category(entry["timelines"]["confirmed"]["history"])
            deaths = Category(entry["timelines"]["deaths"]["history"])
            results.append(initializer(entry, confirmed, deaths))
        return results

    @staticmethod
    def build_jhu_location() -> JhuLocation:
        return JhuLocation(**TestBase.VALID_JHU_LOCATION)

    @staticmethod
    def build_nyt_location() -> NytLocation:
        return NytLocation(**TestBase.VALID_NYT_LOCATION)


class MicroMock(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

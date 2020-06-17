"""Test Base

Class to hold main test utility functions.
"""
import json

from backend.models.classes.category import Category
from backend.models.classes.location import NytLocation


class TestBase:

    TEST_DATE = "2020-05-30"

    SERVICE_LOCATION_FIELDS = ["id", "country", "timelines", "last_updated", "latest"]

    @staticmethod
    def _validate_json_from_file(serializable: object, actual_json_path: str):
        actual = json.dumps(serializable)

        with open(actual_json_path, "r") as f:
            expected = f.read()

        return json.loads(actual) == json.loads(expected)

    @staticmethod
    def _validate_fields(fields, dict):
        for field in fields:
            assert dict[field] is not None

    # TODO: Make this function generic
    @staticmethod
    def _initialize_from_json(path):
        with open(path, "r") as f:
            data = f.read()

        json_data = json.loads(data)

        results = []
        for entry in json_data:
            confirmed = Category(entry["timelines"]["confirmed"]["history"])
            deaths = Category(entry["timelines"]["deaths"]["history"])
            results.append(
                NytLocation(
                    id=entry["id"],
                    country=entry["country"],
                    county=entry["county"],
                    state=entry["state"],
                    fips=entry["fips"],
                    timelines={"confirmed": confirmed, "deaths": deaths,},
                    last_updated=entry["last_updated"],
                    latest=entry["latest"],
                )
            )
        return results

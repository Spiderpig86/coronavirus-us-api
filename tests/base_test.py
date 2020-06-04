"""Test Base

Class to hold main test utility functions.
"""
import json


class TestBase:

    TEST_DATE = "2020-05-30T09:19:06"

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

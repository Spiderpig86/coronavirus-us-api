import json
import os
from unittest import mock

import pytest

from backend.models.classes.category import Category
from backend.models.classes.location import Location, NytLocation
from backend.services.nyt_service import NytDataService
from tests.conftest import mocked_strptime_isoformat

TEST_DATE = "2020-05-30T09:19:06"

fields = [
    "id",
    "country",
    "timelines",
    "last_updated",
    "latest",
    "state",
    "county",
    "fips",
]


@pytest.mark.asyncio
async def test_get_locations_country(mock_web_client):
    await _test_get_data(mock_web_client, "us")


@pytest.mark.asyncio
async def test_get_locations_state(mock_web_client):
    await _test_get_data(mock_web_client, "us-states")


@pytest.mark.asyncio
async def test_get_locations_counties(mock_web_client):
    await _test_get_data(mock_web_client, "us-counties")


async def _test_get_data(mock_web_client, path):
    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        with mock.patch("backend.utils.functions") as functions:
            mock_datetime.utcnow.return_value.isoformat.return_value = TEST_DATE
            mock_datetime.strptime.side_effect = mocked_strptime_isoformat  # Needed since strptime is used in nyt_service
            functions.get_formatted_date.return_value = TEST_DATE

            locations, last_updated = await NytDataService().get_data(
                f"https://raw.githubusercontent.com/nytimes/covid-19-data/master/{path}.csv"
            )

    assert isinstance(locations, list)
    assert isinstance(last_updated, str)

    actual_locations = []
    for location in locations:
        assert isinstance(location, NytLocation)
        assert isinstance(location, Location)

        assert location.country_population != 0

        location_dict = location.to_dict(include_timelines=True)
        assert location_dict is not None
        _validate_fields(fields, location_dict)

        actual_locations.append(location_dict)

    output = json.dumps(actual_locations)

    with open(f"tests/expected/{path}.csv", "r") as f:
        expected = f.read()

    assert json.loads(output) == json.loads(expected)


def _validate_fields(fields, dict):
    for field in fields:
        assert dict[field] is not None

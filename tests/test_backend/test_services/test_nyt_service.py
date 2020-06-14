import json
import os
from unittest import mock

import pytest

from backend.models.classes.category import Category
from backend.models.classes.location import Location, NytLocation
from backend.services.nyt_service import NytDataService
from tests.base_test import TestBase
from tests.conftest import mocked_strptime_isoformat

NYT_FIELDS = {
    *TestBase.SERVICE_LOCATION_FIELDS,
    "state",
    "county",
    "fips",
}


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
    # Arrange
    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        with mock.patch("backend.utils.functions") as functions:
            mock_datetime.utcnow.return_value.isoformat.return_value = (
                TestBase.TEST_DATE
            )
            mock_datetime.strptime.side_effect = mocked_strptime_isoformat  # Needed since strptime is used in nyt_service
            functions.get_formatted_date.return_value = TestBase.TEST_DATE

            # Act
            locations, last_updated = await NytDataService().get_data(
                f"https://raw.githubusercontent.com/nytimes/covid-19-data/master/{path}.csv"
            )

    # Assert
    assert isinstance(locations, list)
    assert isinstance(last_updated, str)
    assert last_updated == f"{TestBase.TEST_DATE}Z"

    actual_locations = []
    for location in locations:
        assert isinstance(location, NytLocation)
        assert isinstance(location, Location)

        assert location.country_population != 0

        location_dict = location.to_dict(include_timelines=True)
        assert location_dict is not None
        TestBase._validate_fields(NYT_FIELDS, location_dict)

        actual_locations.append(location_dict)

    assert TestBase._validate_json_from_file(
        actual_locations, f"tests/expected/service/{path}.json"
    )

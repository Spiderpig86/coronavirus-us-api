import json
import os
from unittest import mock

import pytest

from backend.core.config.constants import DATA_ENDPOINTS
from backend.models.classes.category import Category
from backend.models.classes.location import JhuLocation, Location
from backend.services.jhu_service import JhuDataService
from tests.base_test import TestBase
from tests.conftest import mocked_strptime_isoformat

JHU_FIELDS = {
    *TestBase.SERVICE_LOCATION_FIELDS,
    "state",
    "county",
    "fips",
    "uid",
    "iso2",
    "iso3",
    "code3",
    "state",
    "county",
    "fips",
    "latitude",
    "longitude",
}


@pytest.mark.asyncio
async def test_get_locations(mock_web_client):
    # Arrange & Act
    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        with mock.patch("backend.utils.functions") as functions:
            mock_datetime.utcnow.return_value.isoformat.return_value = (
                TestBase.TEST_DATE
            )
            mock_datetime.strptime.side_effect = mocked_strptime_isoformat  # Needed since strptime is used in nyt_service
            functions.get_formatted_date.return_value = TestBase.TEST_DATE

            locations, last_updated = await JhuDataService().get_data(
                DATA_ENDPOINTS["JhuFacade"]
            )

    # Assert
    assert isinstance(locations, list)
    assert isinstance(last_updated, str)

    actual_locations = []
    for location in locations:
        assert isinstance(location, JhuLocation)
        assert isinstance(location, Location)

        assert location.country_population != 0

        location_dict = location.to_dict(include_timelines=True)
        assert location_dict is not None
        TestBase._validate_fields(JHU_FIELDS, location_dict)

        actual_locations.append(location_dict)

    assert TestBase._validate_json_from_file(
        actual_locations, "tests/expected/service/jhu_raw.json"
    )

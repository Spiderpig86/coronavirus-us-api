import json
import os
from unittest import mock

import pytest

from backend.models.classes.category import Category
from backend.models.classes.location import Location, NytLocation
from backend.services.jhu_service import JhuDataService
from tests.conftest import mocked_strptime_isoformat

TEST_DATE = "2020-05-30T09:19:06"

fields = [
    "id",
    "country",
    "timelines",
    "last_updated",
    "latest",
    "uid",
    "iso2",
    "iso3",
    "code3",
    "state",
    "county",
    "fips",
    "latitude",
    "longitude"
]

@pytest.mark.asyncio
async def test_get_locations(mock_web_client):
    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        with mock.patch("backend.utils.functions") as functions:
            mock_datetime.utcnow.return_value.isoformat.return_value = TEST_DATE
            mock_datetime.strptime.side_effect = mocked_strptime_isoformat  # Needed since strptime is used in nyt_service
            functions.get_formatted_date.return_value = TEST_DATE

            locations, last_updated = await JhuDataService().get_data()

    
"""JHU Facade Test

Test for JHU Facade
"""


import json
from unittest import mock

import pytest

from backend.facades.jhu_facade import JhuFacade
from backend.models.classes.category import Category
from backend.models.classes.location import JhuLocation
from tests.base_test import TestBase
from tests.conftest import mocked_strptime_isoformat

try:  # Pragma AsyncMock
    from unittest.mock import AsyncMock
except ImportError:
    # Python 3.7 and beloqw
    from asyncmock import AsyncMock


@pytest.mark.asyncio
async def test__get_country_data__success(mock_web_client):
    # Arrange
    TEST_JHU_COUNTRY_DATA = TestBase._initialize_from_json(
        "tests/expected/service/jhu_raw.json", _initializer
    )

    jhu_facade = JhuFacade()
    mocked_data_service = AsyncMock()
    mocked_data_service.get_data.return_value = (
        TEST_JHU_COUNTRY_DATA,
        f"{TestBase.TEST_DATE}",
    )
    jhu_facade.DATA_SERVICE = mocked_data_service

    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        with mock.patch("backend.utils.functions") as MockFunctions:
            mock_datetime.utcnow.return_value.strftime.return_value = TestBase.TEST_DATE
            mock_datetime.strptime.side_effect = mocked_strptime_isoformat
            MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

            # Act
            country_data, last_updated = await jhu_facade.get_country_data()

    actual = []
    for location in country_data:
        assert isinstance(location, JhuLocation)
        assert isinstance(location.timelines["confirmed"], Category)
        assert isinstance(location.timelines["deaths"], Category)
        assert isinstance(location.latest, dict)

        actual.append(location.to_dict(include_timelines=True))
    # Assert
    assert TestBase._validate_json_from_file(
        actual, "tests/expected/facade/jhu_country_data.json"
    )


@pytest.mark.asyncio
async def test__get_state_data__success(mock_web_client):
    # Arrange
    TEST_JHU_COUNTRY_DATA = TestBase._initialize_from_json(
        "tests/expected/service/jhu_raw.json", _initializer
    )

    jhu_facade = JhuFacade()
    mocked_data_service = AsyncMock()
    mocked_data_service.get_data.return_value = (
        TEST_JHU_COUNTRY_DATA,
        f"{TestBase.TEST_DATE}",
    )
    jhu_facade.DATA_SERVICE = mocked_data_service

    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        with mock.patch("backend.utils.functions") as MockFunctions:
            mock_datetime.utcnow.return_value.strftime.return_value = TestBase.TEST_DATE
            mock_datetime.strptime.side_effect = mocked_strptime_isoformat
            MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

            # Act
            country_data, last_updated = await jhu_facade.get_state_data()

    actual = []
    for location in country_data:
        assert isinstance(location, JhuLocation)
        assert isinstance(location.timelines["confirmed"], Category)
        assert isinstance(location.timelines["deaths"], Category)
        assert isinstance(location.latest, dict)

        actual.append(location.to_dict(include_timelines=True))

    # Assert
    assert TestBase._validate_json_from_file(
        actual, "tests/expected/facade/jhu_state_data.json"
    )


@pytest.mark.asyncio
async def test__get_county_data__success(mock_web_client):
    # Arrange
    TEST_JHU_COUNTRY_DATA = TestBase._initialize_from_json(
        "tests/expected/service/jhu_raw.json", _initializer
    )

    jhu_facade = JhuFacade()
    mocked_data_service = AsyncMock()
    mocked_data_service.get_data.return_value = (
        TEST_JHU_COUNTRY_DATA,
        f"{TestBase.TEST_DATE}",
    )
    jhu_facade.DATA_SERVICE = mocked_data_service

    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        with mock.patch("backend.utils.functions") as MockFunctions:
            mock_datetime.utcnow.return_value.strftime.return_value = TestBase.TEST_DATE
            mock_datetime.strptime.side_effect = mocked_strptime_isoformat
            MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

            # Act
            country_data, last_updated = await jhu_facade.get_county_data()

    actual = []
    for location in country_data:
        assert isinstance(location, JhuLocation)
        assert isinstance(location.timelines["confirmed"], Category)
        assert isinstance(location.timelines["deaths"], Category)
        assert isinstance(location.latest, dict)

        actual.append(location.to_dict(include_timelines=True))

    # Assert
    assert TestBase._validate_json_from_file(
        actual, "tests/expected/facade/jhu_county_data.json"
    )


def _initializer(entry, confirmed, deaths):
    return JhuLocation(
        id=entry["id"],
        country=entry["country"],
        county=entry["county"],
        state=entry["state"],
        fips=entry["fips"],
        timelines={"confirmed": confirmed, "deaths": deaths,},
        last_updated=entry["last_updated"],
        latest=entry["latest"],
        uid=entry["uid"],
        iso2=entry["iso2"],
        iso3=entry["iso3"],
        code3=entry["code3"],
        latitude=entry["latitude"],
        longitude=entry["longitude"],
    )

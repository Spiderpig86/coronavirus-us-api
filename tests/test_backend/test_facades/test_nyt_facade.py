"""NYT Facade Test

Test for NYT Facade
"""


from unittest import mock

import pytest

from backend.facades.nyt_facade import NytFacade
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
    TEST_NYT_COUNTRY_DATA = TestBase._initialize_from_json(
        "tests/expected/service/us.json"
    )
    print(TEST_NYT_COUNTRY_DATA[0].to_dict())

    nyt_facade = NytFacade()
    mocked_data_service = AsyncMock()
    mocked_data_service.get_data.return_value = (
        TEST_NYT_COUNTRY_DATA,
        f"{TestBase.TEST_DATE}Z",
    )
    nyt_facade.DATA_SERVICE = mocked_data_service

    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        with mock.patch("backend.utils.functions") as MockFunctions:
            mock_datetime.utcnow.return_value.isoformat.return_value = (
                TestBase.TEST_DATE
            )
            mock_datetime.strptime.side_effect = mocked_strptime_isoformat
            MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

            # Act
            country_data, last_updated = await nyt_facade.get_country_data()

    actual = []
    for location in country_data:
        # Testing done in test_nyt_service.py
        # Location object is also already dictionary (no need to test to_dict() again)
        actual.append(location.to_dict(include_timelines=True))

    # Assert
    assert TestBase._validate_json_from_file(
        actual, f"tests/expected/facade/nyt_country_data.json"
    )


@pytest.mark.asyncio
async def test__get_state_data__success():
    # Arrange
    TEST_NYT_COUNTRY_DATA = TestBase._initialize_from_json(
        "tests/expected/service/us-states.json"
    )
    print(TEST_NYT_COUNTRY_DATA[0].to_dict())

    nyt_facade = NytFacade()
    mocked_data_service = AsyncMock()
    mocked_data_service.get_data.return_value = (
        TEST_NYT_COUNTRY_DATA,
        f"{TestBase.TEST_DATE}Z",
    )
    nyt_facade.DATA_SERVICE = mocked_data_service

    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        with mock.patch("backend.utils.functions") as MockFunctions:
            mock_datetime.utcnow.return_value.isoformat.return_value = (
                TestBase.TEST_DATE
            )
            mock_datetime.strptime.side_effect = mocked_strptime_isoformat
            MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

            # Act
            country_data, last_updated = await nyt_facade.get_country_data()

    actual = []
    for location in country_data:
        # Testing done in test_nyt_service.py
        # Location object is also already dictionary (no need to test to_dict() again)
        actual.append(location.to_dict(include_timelines=True))

    # Assert
    assert TestBase._validate_json_from_file(
        actual, f"tests/expected/facade/nyt_state_data.json"
    )


@pytest.mark.asyncio
async def test__get_county_data__success():
    # Arrange
    TEST_NYT_COUNTRY_DATA = TestBase._initialize_from_json(
        "tests/expected/service/us-counties.json"
    )
    print(TEST_NYT_COUNTRY_DATA[0].to_dict())

    nyt_facade = NytFacade()
    mocked_data_service = AsyncMock()
    mocked_data_service.get_data.return_value = (
        TEST_NYT_COUNTRY_DATA,
        f"{TestBase.TEST_DATE}Z",
    )
    nyt_facade.DATA_SERVICE = mocked_data_service

    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        with mock.patch("backend.utils.functions") as MockFunctions:
            mock_datetime.utcnow.return_value.isoformat.return_value = (
                TestBase.TEST_DATE
            )
            mock_datetime.strptime.side_effect = mocked_strptime_isoformat
            MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

            # Act
            country_data, last_updated = await nyt_facade.get_country_data()

    actual = []
    for location in country_data:
        # Testing done in test_nyt_service.py
        # Location object is also already dictionary (no need to test to_dict() again)
        actual.append(location.to_dict(include_timelines=True))

    # Assert
    assert TestBase._validate_json_from_file(
        actual, f"tests/expected/facade/nyt_county_data.json"
    )

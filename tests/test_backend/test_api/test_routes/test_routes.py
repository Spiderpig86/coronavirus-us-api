import pytest
import asyncio
from unittest import mock, TestCase
from async_asgi_testclient import TestClient

from tests.base_test import TestBase
from tests.conftest import mocked_strptime_isoformat, mock_async_api_client
from backend.main import api

def async_test(coroutine):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coroutine(*args, **kwargs))
    return wrapper

@pytest.mark.usefixtures("mock_web_client_class") # Inject webclient into test
@pytest.mark.asyncio
class RoutesTest(TestCase):

    def setUp(self):
        self.client = TestClient(api)
        self.date = TestBase.TEST_DATE

    @async_test
    async def test_county_all(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = TestBase.TEST_DATE
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(f"/api/county/{endpoint}")
        
        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, f"tests/expected/routes/jhu_county_all.json"
        )

    
    @async_test
    async def test_state_all(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = TestBase.TEST_DATE
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(f"/api/state/{endpoint}")
        
        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, f"tests/expected/routes/jhu_state_all.json"
        )

    
    @async_test
    async def test_country_all(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = TestBase.TEST_DATE
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(f"/api/country/{endpoint}")
        
        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, f"tests/expected/routes/jhu_country_all.json"
        )
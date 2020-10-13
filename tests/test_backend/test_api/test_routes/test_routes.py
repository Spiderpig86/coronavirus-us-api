import asyncio
from unittest import TestCase, mock

import pytest
from async_asgi_testclient import TestClient

from backend.main import api
from tests.base_test import TestBase
from tests.conftest import mock_async_api_client, mocked_strptime_isoformat


def async_test(coroutine):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coroutine(*args, **kwargs))

    return wrapper


@pytest.mark.usefixtures("mock_web_client_class")  # Inject webclient into test
@pytest.mark.asyncio
class RoutesTest(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.date = TestBase.TEST_DATE

    #############
    # HEARTBEAT #
    #############
    @async_test
    async def test_heartbeat(self):
        response = await self.client.get("/api/health/heartbeat")

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/heartbeat.json"
        )

    #######
    # ALL #
    #######
    @async_test
    async def test_invalid_source(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(f"/api/county/{endpoint}?source=eee")

        assert response.status_code == 400
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/invalid_source.json"
        )

    @async_test
    async def test_jhu_county_all(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(f"/api/county/{endpoint}?source=jhu")

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/jhu_county_all.json"
        )

    @async_test
    async def test_jhu_state_all(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(f"/api/state/{endpoint}?source=jhu")

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/jhu_state_all.json"
        )

    @async_test
    async def test_jhu_country_all(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(f"/api/country/{endpoint}?source=jhu")

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/jhu_country_all.json"
        )

    @async_test
    async def test_nyt_county_all_with_properties(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(
                    f"/api/county/{endpoint}?source=nyt&timelines=true&properties=true"
                )

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/nyt_county_all.json"
        )

    @async_test
    async def test_nyt_state_all_with_properties(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(
                    f"/api/state/{endpoint}?source=nyt&timelines=true&properties=true"
                )

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/nyt_state_all.json"
        )

    @async_test
    async def test_nyt_country_all_with_properties(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(
                    f"/api/country/{endpoint}?source=nyt&timelines=true&properties=true"
                )

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/nyt_country_all.json"
        )

    # TODO: Parameterize this and add in nyt
    @async_test
    async def test_jhu_country_all_with_unsanitized_params(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(
                    f"/api/country/{endpoint}?source=jhu&__private__=__secret__"
                )

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/jhu_country_all.json"
        )

    @async_test
    async def test_jhu_state_all_with_unsanitized_params(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(
                    f"/api/state/{endpoint}?source=jhu&__private__=__secret__"
                )

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/jhu_state_all.json"
        )

    @async_test
    async def test_nyt_all_with_county_param(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(
                    f"/api/county/{endpoint}?county=snohomish"
                )

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/nyt_with_county_all.json"
        )

    @async_test
    async def test_nyt_county_all_with_state_param(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(
                    f"/api/county/{endpoint}?state=Washington&timelines=true&properties=true"
                )

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/nyt_county_route_with_state_all.json"
        )

    @async_test
    async def test_nyt_county_all_with_state_abbr_param(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(
                    f"/api/county/{endpoint}?state=CA&timelines=true&properties=true"
                )

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/nyt_county_route_with_state_abbr_all.json"
        )

    @async_test
    async def test_nyt_state_all_with_state_param(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(
                    f"/api/state/{endpoint}?state=Washington&timelines=true&properties=true"
                )

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/nyt_state_route_with_state_all.json"
        )

    @async_test
    async def test_nyt_state_all_with_state_abbr_param(self):
        endpoint = "all"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(
                    f"/api/state/{endpoint}?state=CA&timelines=true&properties=true"
                )

        assert response
        actual = response.json()
        print(actual)

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/nyt_state_route_with_state_abbr_all.json"
        )

    ##########
    # LATEST #
    ##########
    @async_test
    async def test_jhu_country_latest(self):
        endpoint = "latest"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(f"/api/country/{endpoint}?source=jhu")

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/jhu_country_latest.json"
        )

    @async_test
    async def test_nyt_country_latest(self):
        endpoint = "latest"

        with mock.patch("backend.utils.functions.datetime") as mock_datetime:
            with mock.patch("backend.utils.functions") as MockFunctions:
                mock_datetime.utcnow.return_value.strftime.return_value = (
                    TestBase.TEST_DATE
                )
                mock_datetime.strptime.side_effect = mocked_strptime_isoformat
                MockFunctions.get_formatted_date.return_value = TestBase.TEST_DATE

                response = await self.client.get(f"/api/country/{endpoint}")

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/nyt_country_latest.json"
        )

    ###########
    # SOURCES #
    ###########
    @async_test
    async def test_sources(self):
        response = await self.client.get("/api/data/sources")

        assert response
        actual = response.json()

        assert TestBase._validate_json_from_file_str(
            actual, "tests/expected/routes/sources.json"
        )

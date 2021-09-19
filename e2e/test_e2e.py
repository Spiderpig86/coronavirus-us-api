import asyncio
from multiprocessing import Process

import aiohttp
import asynctest
import pytest
import uvicorn


class E2ETestClient(asynctest.TestCase):

    HOST = "127.0.0.1"
    LOCALHOST = "localhost"
    PORT = 5000
    LOG_LEVEL = "info"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        asyncio.get_event_loop().run_until_complete(cls.asyncSetupClass())

    @classmethod
    async def asyncSetupClass(cls):
        cls.process = Process(
            target=uvicorn.run,
            args=("backend.main:api",),
            kwargs={
                "host": cls.HOST,
                "port": cls.PORT,
                "log_level": cls.LOG_LEVEL,
            },
            daemon=True,
        )

        cls.process.start()
        await asyncio.sleep(0.5) # Server may start up late

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.process.terminate()

    @pytest.mark.asyncio
    async def test_heartbeat_success(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://{self.LOCALHOST}:{self.PORT}/api/health/heartbeat"
            ) as response:
                assert response.status == 200
                data = await response.json()

        assert data == {"is_alive": True}

    @pytest.mark.asyncio
    async def test_sources_success(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://{self.LOCALHOST}:{self.PORT}/api/data/sources"
            ) as response:
                assert response.status == 200
                data = await response.json()

        assert data == {"sources": ["nyt", "jhu"]}

    @pytest.mark.asyncio
    async def test_county_all_with_parameters_success(self):
        # Arrange
        async with aiohttp.ClientSession() as session:
            # Act
            async with session.get(
                f"http://{self.LOCALHOST}:{self.PORT}/api/county/all?properties=true&timelines=true"
            ) as response:

                # Assert
                assert response.status == 200
                data = await response.json()

        self._validate_all_fields(data)

    @pytest.mark.asyncio
    async def test_state_all_with_parameters_success(self):
        # Arrange
        async with aiohttp.ClientSession() as session:
            # Act
            async with session.get(
                f"http://{self.LOCALHOST}:{self.PORT}/api/state/all?properties=true&timelines=true"
            ) as response:

                # Assert
                assert response.status == 200
                data = await response.json()

        self._validate_all_fields(data)

    @pytest.mark.asyncio
    async def test_country_all_with_parameters_success(self):
        # Arrange
        async with aiohttp.ClientSession() as session:
            # Act
            async with session.get(
                f"http://{self.LOCALHOST}:{self.PORT}/api/country/all?properties=true&timelines=true"
            ) as response:

                # Assert
                assert response.status == 200
                data = await response.json()

        self._validate_all_fields(data)

    @pytest.mark.asyncio
    async def test_country_latest(self):
        # Arrange
        async with aiohttp.ClientSession() as session:
            # Act
            async with session.get(
                f"http://{self.LOCALHOST}:{self.PORT}/api/country/latest"
            ) as response:

                # Assert
                assert response.status == 200
                data = await response.json()

        assert data.get("latest", None) is not None
        assert data.get("last_updated", None) is not None

    def _validate_all_fields(self, data: dict):
        assert data.get("latest", None) is not None
        assert data.get("locations", None) is not None

        for location in data["locations"]:
            if "Unknown" not in location["id"]:
                assert location.get("properties", None) is not None
                assert location["properties"].get("coordinates", None) is not None

            assert location.get("timelines", None) is not None
            assert location["timelines"].get("confirmed", None) is not None
            assert location["timelines"]["confirmed"].get("history", None) is not None
            assert (
                location["timelines"]["confirmed"].get("latest", None) is not None
            )  # Numeric values can be 0, so we need to have an extra check to make sure it is none
            assert location["timelines"].get("deaths", None) is not None
            assert location["timelines"]["deaths"].get("history", None) is not None
            assert location["timelines"]["deaths"].get("latest", None) is not None

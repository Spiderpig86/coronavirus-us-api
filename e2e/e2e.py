import asyncio
from multiprocessing import Process

import aiohttp
import asynctest
import pytest
import uvicorn


class E2ETestClient(asynctest.TestCase):

    HOST = "127.0.0.1"
    PORT = 5000
    LOG_LEVEL = "info"

    async def setUp(self):
        self.process = Process(
            target=uvicorn.run,
            args=("backend.main:api",),
            kwargs={"host": self.HOST, "port": self.PORT, "log_level": self.LOG_LEVEL},
            daemon=True,
        )

        self.process.start()
        await asyncio.sleep(0.5)

    async def tearDown(self):
        self.process.terminate()

    async def test_heartbeat_success(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://{self.HOST}:{self.PORT}/api/health/heartbeat"
            ) as response:
                assert response.status == 200
                data = await response.json()

        assert data == {"is_alive": True}

    async def test_sources_success(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://{self.HOST}:{self.PORT}/api/data/sources"
            ) as response:
                assert response.status == 200
                data = await response.json()

        assert data == {"sources": ["nyt", "jhu"]}

    async def test_county_all_with_parameters_success(self):
        # Arrange
        async with aiohttp.ClientSession() as session:
            # Act
            async with session.get(
                f"http://{self.HOST}:{self.PORT}/api/county/all?properties=true&timelines=true"
            ) as response:

                # Assert
                assert response.status == 200
                data = await response.json()

        self._validate_all_fields(data)

    async def test_state_all_with_parameters_success(self):
        # Arrange
        async with aiohttp.ClientSession() as session:
            # Act
            async with session.get(
                f"http://{self.HOST}:{self.PORT}/api/state/all?properties=true&timelines=true"
            ) as response:

                # Assert
                assert response.status == 200
                data = await response.json()

        self._validate_all_fields(data)

    async def test_country_all_with_parameters_success(self):
        # Arrange
        async with aiohttp.ClientSession() as session:
            # Act
            async with session.get(
                f"http://{self.HOST}:{self.PORT}/api/country/all?properties=true&timelines=true"
            ) as response:

                # Assert
                assert response.status == 200
                data = await response.json()

        self._validate_all_fields(data)

    async def test_counrty_latest(self):
        # Arrange
        async with aiohttp.ClientSession() as session:
            # Act
            async with session.get(
                f"http://{self.HOST}:{self.PORT}/api/country/latest"
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

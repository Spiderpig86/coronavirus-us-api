import datetime
import os
from contextlib import asynccontextmanager  # Used for allowing "with" keyword

import pytest
from async_asgi_testclient import TestClient as AsyncTestClient
from fastapi.testclient import TestClient

from backend.core.libs import webclient
from backend.main import api

try:  # Pragma AsyncMock
    from unittest.mock import AsyncMock
except ImportError:
    # Python 3.7 and beloqw
    from asyncmock import AsyncMock


class MockedWebClientGetResponse:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename

    async def text(self):
        return self._read_file(self.filename)

    def _read_file(self, filename: str) -> str:

        filepath = os.path.join(os.path.dirname(__file__), f"test_data/{filename}.csv")

        with open(filepath, "r") as f:
            return f.read()


@pytest.fixture
async def mock_web_client():
    """Creates a mocked webclient in place of regular webclient when injected into test.
    """
    webclient.WEBCLIENT = (
        AsyncMock()
    )  # Required to mock async functions https://docs.python.org/3/library/unittest.mock.html
    webclient.WEBCLIENT.get = mocked_session_get  # Replace get functions

    try:
        yield webclient.WEBCLIENT
    finally:
        del webclient.WEBCLIENT  # Teardown


@asynccontextmanager
async def mocked_session_get(*args, **kwargs):
    """Mocks response when calling get() on WEBCLIENT.

    Added @asynccontextmanager since we use context manager in code using "with" keyword
    """

    url = args[0]
    filename = url.split("/")[-1].replace(".csv", "")

    yield MockedWebClientGetResponse(url, filename)


@pytest.fixture
def mock_api_client():
    return TestClient(api)


@pytest.fixture
def mock_async_api_client():
    return AsyncTestClient(api)


@pytest.fixture
def mock_dev_environent():
    pass


@pytest.fixture
def mock_prod_environment():
    pass


class MockedStrpDateTime:
    def __init__(self, date, strformat):
        self.date = date
        self.strformat = strformat

    def isoformat(self):
        return datetime.datetime.strptime(self.date, self.strformat).isoformat()

    def strftime(self, fmt):
        return datetime.datetime.strptime(self.date, self.strformat).strftime(fmt)


def mocked_strptime_isoformat(*args, **kwargs):
    """Returns a mocked instance of a datetime.strp object.

    Returns:
        MockedStrDateTime -- mocked datetime.strp object.
    """
    date = args[0]
    strformat = args[1]

    return MockedStrpDateTime(date, strformat)

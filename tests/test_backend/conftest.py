import os

from backend.core.utils import webclient

try:  # Pragma AsyncMock
    from unittest.mock import AsyncMock
except ImportError:
    # Python 3.7 and beloqw
    from asyncmock import AsyncMock

from contextlib import asynccontextmanager  # Used for allowing "with" keyword


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

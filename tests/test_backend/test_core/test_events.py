"""Events Test

Events unit test.
"""
import pytest

from backend.core.events import shutdown_handler, startup_handler
from backend.core.libs import webclient


def test__event_handlers__success():
    # Arrange & Act
    startup_function = startup_handler(None)  # It is ok pass app as None for now
    shutdown_function = shutdown_handler(None)

    # Assert
    assert callable(startup_function)
    assert callable(shutdown_function)


@pytest.mark.asyncio
async def test__call_event_handlers__success():
    # Arrange
    startup_function = startup_handler(None)  # It is ok pass app as None for now
    shutdown_function = shutdown_handler(None)

    # Act & Assert
    await startup_function()
    assert webclient.WEBCLIENT

    await shutdown_function()
    assert webclient.WEBCLIENT.closed

    del webclient.WEBCLIENT

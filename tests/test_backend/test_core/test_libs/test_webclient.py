"""WebClient Test

WebClient unit test.
"""
import pytest

from backend.core.libs import webclient


@pytest.mark.asyncio
async def test__webclient_lifecycle__success():
    with pytest.raises(AttributeError):
        # Uninitialized webclient
        webclient.WEBCLIENT

    # Setup
    await webclient.setup_webclient()
    assert webclient.WEBCLIENT

    # Teardown
    await webclient.teardown_webclient()
    assert webclient.WEBCLIENT.closed

    del webclient.WEBCLIENT

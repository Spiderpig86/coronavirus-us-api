import asyncio
import time

import pytest

from backend.utils.function_timer import async_timed, timed


def test__timed_decorator__success():
    @timed("test__timed_decorator__success")
    def _test_function():
        time.sleep(1)

    _test_function()


@pytest.mark.asyncio
async def test__async_timed_decorator__success():
    @timed("test__async_timed_decorator__success")
    async def _async_test_function():
        await asyncio.sleep(1)

    await _async_test_function()

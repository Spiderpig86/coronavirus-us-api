import asyncio
from multiprocessing import Process

import aiohttp
import asynctest
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

    async def test__heartbeat__success(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://127.0.0.1:{self.PORT}/api/health/heartbeat"
            ) as response:
                data = await response.json()
        assert data == {"is_alive": True}

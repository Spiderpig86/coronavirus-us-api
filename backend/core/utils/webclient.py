"""WebClient

Singleton wrapper around aiohttp. Reuse same client instead of creating a new instance every time.
"""
from aiohttp import ClientSession, ClientTimeout
from loguru import logger

WEBCLIENT: ClientSession

async def setup_webclient():
    """Create webclient wrapper for the api lifespan.
    """
    global WEBCLIENT
    logger.info('Setting up WebClient...')
    WEBCLIENT = ClientSession(timeout=ClientTimeout(total=60))

async def teardown_webclient():
    """Cleanup webclient.
    """
    global WEBCLIENT
    logger.info('Cleaning up WebClient...')
    await WEBCLIENT.close()
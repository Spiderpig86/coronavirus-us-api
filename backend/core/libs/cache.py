"""Cache

Library in charge of managing application cache.
"""
from typing import Union

import aiocache
from loguru import logger

from backend.core.config.constants import REDIS_URL, STAGE


class Cache:
    def __init__(self):
        self.cache = self._build_cache()

    def _build_cache(self) -> Union[aiocache.RedisCache, aiocache.SimpleMemoryCache]:
        if STAGE and STAGE == "prod" and REDIS_URL:  # TODO: Refactor to util?
            logger.info("Initializing RedisCloud Cache...")
            return aiocache.RedisCache(
                endpoint=REDIS_URL.host,
                port=REDIS_URL.port,
                password=REDIS_URL.password,
                create_connection_timeout=5,
            )
        else:
            logger.info("Initializing SimpleMemoryCache...")
            return aiocache.SimpleMemoryCache()

    async def get_item(self, item_id: str) -> object:
        result = await self.cache.get(item_id)
        logger.info(
            "Cache " + ("hit " if result else "miss ") + f"for item id {item_id}"
        )
        await self.cache.close()
        return result

    async def set_item(self, item_id: str, item: object, ttl: int = 3600):
        await self.cache.set(item_id, item, ttl)
        logger.info(f"Cache set with item id {item_id}")
        await self.cache.close()

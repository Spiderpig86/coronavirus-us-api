"""Cache

Library in charge of managing application cache.
"""
import json
import sys
import zlib
from base64 import b64decode, b64encode
from typing import Union

import aiocache
from aiocache.serializers import BaseSerializer
from loguru import logger

from backend.core.config.constants import REDIS_CACHE_TIMEOUT_SECONDS


class Cache:
    def __init__(self, stage=None, redis_url=None):
        self.stage = stage
        self.redis_url = redis_url
        self.cache = self._build_cache()

    def _build_cache(self) -> Union[aiocache.RedisCache, aiocache.SimpleMemoryCache]:
        if (
            self.stage and self.stage == "prod" and self.redis_url
        ):  # TODO: Refactor to util?
            logger.info("Initializing RedisCloud Cache...")
            return aiocache.RedisCache(
                endpoint=self.redis_url.hostname,
                port=self.redis_url.port,
                password=self.redis_url.password,
                create_connection_timeout=5,
                serializer=CacheCompressionSerializer(),
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

    async def set_item(
        self, item_id: str, item: object, ttl: int = REDIS_CACHE_TIMEOUT_SECONDS
    ):
        if item:
            await self.cache.set(item_id, item, ttl)
            logger.info(f"Cache set with item id {item_id} with ttl {ttl} seconds")
        await self.cache.close()


""" Cache serializer that supports compression. """


class CacheCompressionSerializer(BaseSerializer):

    # This is needed because zlib works with bytes.
    # this way the underlying backend knows how to
    # store/retrieve values
    DEFAULT_ENCODING = None

    def dumps(self, value):
        compressed = self._serialize(value)
        return compressed

    def loads(self, value):
        if not value:
            return None
        return self._deserialize(value)

    def _serialize(self, item: object):
        serialized = json.dumps(item).encode()
        compressed = zlib.compress(serialized)
        # compressed = b64encode(compressed).decode('ascii')
        return compressed

    def _deserialize(self, item: bytes):
        # decompressed = json.loads(zlib.decompress(b64decode(item)))
        decompressed = json.loads(zlib.decompress(item))
        return decompressed

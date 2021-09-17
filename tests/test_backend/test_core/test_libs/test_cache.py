"""Cache Test

Cache unit test.
"""
import os
from unittest import mock
from urllib.parse import urlparse

import aiocache
import pytest

from backend.core.libs.cache import Cache, CacheCompressionSerializer

CACHE_COMPRESSION_VALID_UNSERIALIZED_INPUT = {"foo": "bar"}
CACHE_COMPRESSION_VALID_SERIALIZED_INPUT = (
    b"x\x9c\xabVJ\xcb\xcfW\xb2RPJJ,R\xaa\x05\x00 \x98\x04T"
)


def test__stage_dev__build_cache__success():
    with mock.patch("backend.core.config.constants.STAGE", "dev"):
        cache = Cache()._build_cache()

    assert isinstance(cache, aiocache.SimpleMemoryCache)


def test__missing_redis_url__build_cache__success():
    cache = Cache("prod", None)._build_cache()
    assert isinstance(cache, aiocache.SimpleMemoryCache)


def test__stage_prod__build_cache__success():
    cache = Cache(
        "prod",
        urlparse(
            "redis://rediscloud:test@redis-123.c80.us-west-1-2.ec2.cloud.redislabs.com:12345"
        ),
    )._build_cache()

    assert isinstance(cache, aiocache.RedisCache)


def test__dumps__normal_input__success():
    # Arrange
    serializer = CacheCompressionSerializer()

    # Act & Assert
    assert (
        serializer.dumps(CACHE_COMPRESSION_VALID_UNSERIALIZED_INPUT)
        == CACHE_COMPRESSION_VALID_SERIALIZED_INPUT
    )


def test__loads__normal_input__success():
    # Arrange
    serializer = CacheCompressionSerializer()

    # Act & Assert
    assert (
        serializer.loads(CACHE_COMPRESSION_VALID_SERIALIZED_INPUT)
        == CACHE_COMPRESSION_VALID_UNSERIALIZED_INPUT
    )
    assert (
        serializer.loads(serializer.dumps(CACHE_COMPRESSION_VALID_UNSERIALIZED_INPUT))
        == CACHE_COMPRESSION_VALID_UNSERIALIZED_INPUT
    )


def test__loads__none_input__success():
    # Arrange
    serializer = CacheCompressionSerializer()

    # Act & Assert
    assert serializer.loads(None) is None


@pytest.mark.asyncio
async def test__get_set_item__success():
    # Arrange
    cache = Cache()
    cache._build_cache()
    await cache.set_item("foo", "bar", 300)

    # Act & Assert
    assert await cache.get_item("foo") == "bar"

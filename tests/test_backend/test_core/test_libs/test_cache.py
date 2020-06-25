"""Cache Test

Cache unit test.
"""
import os
from unittest import mock
from urllib.parse import urlparse

import aiocache

from backend.core.libs.cache import Cache


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


def test__get_set_item__success():
    # Arrange
    cache = Cache()._build_cache()
    cache.set_item("foo", "bar", 300)

    # Act & Assert
    assert cache.get_item("foo") == "bar"

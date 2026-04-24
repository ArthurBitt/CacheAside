import pytest
from unittest.mock import AsyncMock

from redis_patterns.settings import CacheSettings
from redis_patterns.cacheaside.cache import CacheAside

@pytest.mark.asyncio
async def test_get_or_set_cache_hit():
    settings = CacheSettings(redis_url="redis://dummy")
    redis_client = AsyncMock()
    redis_client.get = AsyncMock(return_value='{"id": 1}')
    redis_client.set = AsyncMock()

    cache = CacheAside(settings=settings, redis_client=redis_client)

    async def fetcher():
        raise AssertionError("fetcher não deveria ser chamado em cache HIT")

    result = await cache.get_or_set("item", "1", fetcher)

    assert result["hit"] is True
    assert result["value"] == {"id": 1}
    redis_client.set.assert_not_called()

@pytest.mark.asyncio
async def test_get_or_set_cache_miss_sets_value():
    settings = CacheSettings(redis_url="redis://dummy", default_ttl_seconds=60)
    redis_client = AsyncMock()
    redis_client.get = AsyncMock(return_value=None)
    redis_client.set = AsyncMock()

    cache = CacheAside(settings=settings, redis_client=redis_client)

    async def fetcher():
        return {"id": 2}

    result = await cache.get_or_set("item", "2", fetcher)

    assert result["hit"] is False
    assert result["value"] == {"id": 2}
    redis_client.set.assert_called_once()  # setou o cache
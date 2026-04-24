import pytest
from unittest.mock import AsyncMock

from redis_patterns.settings import CacheSettings
from redis_patterns.cacheaside.cache import CacheAside

@pytest.mark.asyncio
async def test_invalidate_deletes_key():
    settings = CacheSettings(redis_url="redis://dummy")
    redis_client = AsyncMock()
    redis_client.delete = AsyncMock(return_value=1)

    cache = CacheAside(settings=settings, redis_client=redis_client)

    deleted = await cache.invalidate("item", "123")

    assert deleted == 1
    redis_client.delete.assert_called_once_with("cache:v1:item:123")
from __future__ import annotations

from typing import Any, Awaitable, Callable, Optional

import redis.asyncio as redis

from redis_patterns.settings import CacheSettings
from redis_patterns.keys import make_cache_key
from redis_patterns.codec import JsonCodec


class CacheAside:
    def __init__(
        self,
        *,
        settings: CacheSettings,
        redis_client: redis.Redis,
        codec: Optional[JsonCodec] = None,
    ):
        self.settings = settings
        self.redis = redis_client
        self.codec = codec or JsonCodec()

    def key(self, resource: str, identifier: str) -> str:
        return make_cache_key(
            resource,
            identifier,
            prefix=self.settings.prefix,
            version=self.settings.version,
            namespace=self.settings.namespace,
        )

    async def get_or_set(
        self,
        resource: str,
        identifier: str,
        fetcher: Callable[[], Awaitable[Any]],
        ttl_seconds: Optional[int] = None,
    ) -> dict:
        key = self.key(resource, identifier)
        ttl = ttl_seconds or self.settings.default_ttl_seconds

        # 1) tenta cache
        try:
            cached = await self.redis.get(key)
            if cached is not None:
                return {"hit": True, "value": self.codec.loads(cached)}
        except Exception:
            if not self.settings.fail_open:
                raise

        # 2) miss -> busca da fonte (Postgres)
        value = await fetcher()

        # 3) tenta setar cache
        try:
            await self.redis.set(key, self.codec.dumps(value), ex=ttl)
        except Exception:
            if not self.settings.fail_open:
                raise

        return {"hit": False, "value": value}

    async def invalidate(self, resource: str, identifier: str) -> int:
        # delega para o módulo de invalidation
        from .invalidation import invalidate_one
        return await invalidate_one(self, resource, identifier)

    async def close(self) -> None:
        await self.redis.aclose()
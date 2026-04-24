from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cache import CacheAside


async def invalidate_one(cache: "CacheAside", resource: str, identifier: str) -> int:
    """
    Invalida 1 chave (modo simples).
    Deve ser chamado após commit do update no Postgres.
    Retorna quantidade de chaves removidas (0 ou 1).
    """
    key = cache.key(resource, identifier)
    try:
        return await cache.redis.delete(key)
    except Exception:
        if not cache.settings.fail_open:
            raise
        return 0
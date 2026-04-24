from dataclasses import dataclass

@dataclass(frozen=True)
class CacheSettings:
    redis_url: str
    prefix: str = "cache"
    version: str = "v1"
    namespace: str | None = None  # ex.: "prod", "stg"
    default_ttl_seconds: int = 60
    fail_open: bool = True

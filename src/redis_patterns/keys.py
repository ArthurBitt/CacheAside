def make_cache_key(
    resource: str,
    identifier: str,
    *,
    prefix: str = "cache",
    version: str = "v1",
    namespace: str | None = None,
) -> str:
    parts = []
    if namespace:
        parts.append(namespace)
    parts.extend([prefix, version, resource, identifier])
    return ":".join(parts)

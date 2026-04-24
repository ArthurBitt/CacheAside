import redis.asyncio as redis

def create_redis_client(redis_url: str, *, decode_responses: bool = True) -> redis.Redis:
    return redis.Redis.from_url(redis_url, decode_responses=decode_responses)
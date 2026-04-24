from redis_patterns import make_cache_key

def test_make_cache_key():
    assert make_cache_key("item","1") == "cache:v1:item:1"


def test_make_cache_key_namespace():
    assert make_cache_key("item", "1", namespace="prod") == "prod:cache:v1:item:1"


def test_make_cache_key_custom_prefix_version():
    assert make_cache_key("item", "1", prefix="c", version="v2") == "c:v2:item:1"

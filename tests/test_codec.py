from redis_patterns.codec import JsonCodec

def test_codec_roundtrip_dict():
    codec = JsonCodec()
    data = {"id": 1, "name": "item-1"}
    raw = codec.dumps(data)
    assert codec.loads(raw) == data
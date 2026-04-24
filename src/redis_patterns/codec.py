import json
from typing import Any

class JsonCodec:
    def dumps(self, value: Any) -> str:
        return json.dumps(value, default=self._default)

    def loads(self, raw: str) -> Any:
        return json.loads(raw)

    def _default(self, obj: Any):
        # Pydantic v2
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        # Pydantic v1
        if hasattr(obj, "dict"):
            return obj.dict()
        # dataclass/obj simples
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

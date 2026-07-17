"""In-memory TTL cache (Section 20.13). A demo-scale single-process cache
is sufficient here; a real deployment would back this with Redis."""
from __future__ import annotations

import time
from threading import Lock
from typing import Any


class TTLCache:
    def __init__(self, ttl_minutes: int):
        self._ttl_seconds = ttl_minutes * 60
        self._store: dict[str, tuple[float, Any]] = {}
        self._lock = Lock()

    def get(self, key: str) -> Any | None:
        with self._lock:
            entry = self._store.get(key)
            if not entry:
                return None
            expires_at, value = entry
            if time.time() > expires_at:
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._store[key] = (time.time() + self._ttl_seconds, value)

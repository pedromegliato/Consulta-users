import json
from dataclasses import asdict
from typing import Any

from redis.asyncio import Redis

from app.domain.user import User

KEY_PREFIX = "user:"


class RedisUserCache:
    def __init__(self, client: Redis, ttl_seconds: int) -> None:
        self._client = client
        self._ttl_seconds = ttl_seconds

    async def get(self, user_id: int) -> User | None:
        raw = await self._client.get(_key(user_id))
        if raw is None:
            return None
        payload: dict[str, Any] = json.loads(raw)
        return User(**payload)

    async def set(self, user: User) -> None:
        await self._client.set(_key(user.id), json.dumps(asdict(user)), ex=self._ttl_seconds)


def _key(user_id: int) -> str:
    return f"{KEY_PREFIX}{user_id}"

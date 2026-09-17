import time

from app.domain.user import User


class InMemoryUserCache:
    def __init__(self, ttl_seconds: int) -> None:
        self._ttl_seconds = ttl_seconds
        self._entries: dict[int, tuple[float, User]] = {}

    async def get(self, user_id: int) -> User | None:
        entry = self._entries.get(user_id)
        if entry is None:
            return None

        expires_at, user = entry
        if expires_at <= time.monotonic():
            del self._entries[user_id]
            return None
        return user

    async def set(self, user: User) -> None:
        self._entries[user.id] = (time.monotonic() + self._ttl_seconds, user)

from app.domain.ports import UserCache, UserProvider
from app.domain.user import User


class CachedUserProvider:
    def __init__(self, cache: UserCache, delegate: UserProvider) -> None:
        self._cache = cache
        self._delegate = delegate

    async def get_user(self, user_id: int) -> User:
        cached = await self._cache.get(user_id)
        if cached is not None:
            return cached

        user = await self._delegate.get_user(user_id)
        await self._cache.set(user)
        return user

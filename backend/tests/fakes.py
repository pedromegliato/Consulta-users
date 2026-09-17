import asyncio
from collections.abc import Mapping

from app.domain.exceptions import ProviderError, UserNotFoundError
from app.domain.user import User

Outcome = User | Exception


class FakeUserProvider:
    """Provider em memoria que registra concorrencia observada e chamadas recebidas."""

    def __init__(self, outcomes: Mapping[int, Outcome], delay_seconds: float = 0.0) -> None:
        self._outcomes = outcomes
        self._delay_seconds = delay_seconds
        self.calls: list[int] = []
        self.max_in_flight = 0
        self._in_flight = 0

    async def get_user(self, user_id: int) -> User:
        self.calls.append(user_id)
        self._in_flight += 1
        self.max_in_flight = max(self.max_in_flight, self._in_flight)
        try:
            if self._delay_seconds:
                await asyncio.sleep(self._delay_seconds)
            outcome = self._outcomes.get(user_id)
            if outcome is None:
                raise UserNotFoundError(user_id)
            if isinstance(outcome, Exception):
                raise outcome
            return outcome
        finally:
            self._in_flight -= 1


class FakeUserRepository:
    def __init__(self, stored: dict[int, User] | None = None) -> None:
        self.stored = dict(stored or {})

    async def find(self, user_id: int) -> User | None:
        return self.stored.get(user_id)

    async def save(self, user: User) -> None:
        self.stored[user.id] = user


class FakeUserCache:
    def __init__(self) -> None:
        self.entries: dict[int, User] = {}

    async def get(self, user_id: int) -> User | None:
        return self.entries.get(user_id)

    async def set(self, user: User) -> None:
        self.entries[user.id] = user


class AlwaysFailingProvider:
    def __init__(self, error: ProviderError) -> None:
        self._error = error
        self.calls = 0

    async def get_user(self, user_id: int) -> User:
        self.calls += 1
        raise self._error

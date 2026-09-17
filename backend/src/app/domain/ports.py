from typing import Protocol

from app.domain.pagination import Page
from app.domain.queries import UserQuery
from app.domain.user import User


class UserProvider(Protocol):
    """Fonte de usuários. Levanta ProviderError quando o usuário não pode ser resolvido."""

    async def get_user(self, user_id: int) -> User: ...


class UserCache(Protocol):
    async def get(self, user_id: int) -> User | None: ...

    async def set(self, user: User) -> None: ...


class UserRepository(Protocol):
    async def find(self, user_id: int) -> User | None: ...

    async def save(self, user: User) -> None: ...


class UserQueryRepository(Protocol):
    async def search(self, query: UserQuery) -> Page[User]: ...


class UserStore(UserRepository, UserQueryRepository, Protocol): ...

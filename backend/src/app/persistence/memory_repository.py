from operator import attrgetter

from app.domain.pagination import Page, SortDirection
from app.domain.queries import UserQuery
from app.domain.text import phone_search_digits
from app.domain.user import User


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: dict[int, User] = {}

    async def find(self, user_id: int) -> User | None:
        return self._users.get(user_id)

    async def save(self, user: User) -> None:
        self._users[user.id] = user

    async def search(self, query: UserQuery) -> Page[User]:
        matches = [user for user in self._users.values() if _matches(user, query.search)]
        matches.sort(
            key=attrgetter(query.sort_by.value),
            reverse=query.sort_direction is SortDirection.DESC,
        )
        window = matches[query.offset : query.offset + query.page_size]
        return Page(
            items=window,
            total=len(matches),
            page=query.page,
            page_size=query.page_size,
        )


def _matches(user: User, search: str | None) -> bool:
    if not search:
        return True

    term = search.casefold()
    text_fields = (str(user.id), user.name, user.username, user.email)
    if any(term in field.casefold() for field in text_fields):
        return True

    digits = phone_search_digits(search)
    return digits is not None and user.phone is not None and digits in user.phone

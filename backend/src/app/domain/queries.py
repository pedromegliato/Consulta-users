from dataclasses import dataclass
from enum import Enum

from app.domain.pagination import DEFAULT_PAGE_SIZE, SortDirection


class UserSortField(str, Enum):
    ID = "id"
    NAME = "name"
    USERNAME = "username"
    EMAIL = "email"


@dataclass(frozen=True)
class UserQuery:
    search: str | None = None
    sort_by: UserSortField = UserSortField.ID
    sort_direction: SortDirection = SortDirection.ASC
    page: int = 1
    page_size: int = DEFAULT_PAGE_SIZE

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

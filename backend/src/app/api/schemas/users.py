from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.application.fetch_users import FetchUsersResult
from app.domain.pagination import (
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    MIN_PAGE,
    MIN_PAGE_SIZE,
    Page,
    SortDirection,
)
from app.domain.queries import UserQuery, UserSortField
from app.domain.user import User

MAX_USER_IDS_PER_REQUEST = 100
MAX_SEARCH_LENGTH = 120

UserId = Annotated[int, Field(gt=0)]


class FetchUsersRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"examples": [{"user_ids": [1, 2, 3, 4]}]},
    )

    user_ids: Annotated[
        list[UserId],
        Field(
            min_length=1,
            max_length=MAX_USER_IDS_PER_REQUEST,
            description="IDs inteiros positivos. Repetidos são consultados uma única vez.",
        ),
    ]


class UserPayload(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int
    name: str
    username: str
    email: str
    phone: str | None = Field(default=None, description="Somente dígitos, sem ramal.")

    @classmethod
    def from_domain(cls, user: User) -> "UserPayload":
        return cls(
            id=user.id,
            name=user.name,
            username=user.username,
            email=user.email,
            phone=user.phone,
        )


class FetchUsersResponse(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "examples": [
                {
                    "users": [
                        {
                            "id": 1,
                            "name": "Leanne Graham",
                            "username": "Bret",
                            "email": "sincere@april.biz",
                            "phone": "17707368031",
                        }
                    ],
                    "failed": [3, 4],
                }
            ]
        },
    )

    users: list[UserPayload]
    failed: list[int] = Field(description="IDs que não puderam ser resolvidos.")

    @classmethod
    def from_result(cls, result: FetchUsersResult) -> "FetchUsersResponse":
        return cls(
            users=[UserPayload.from_domain(user) for user in result.users],
            failed=result.failed,
        )


class ListUsersParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    search: Annotated[
        str | None,
        Field(
            default=None,
            max_length=MAX_SEARCH_LENGTH,
            description="Filtra por nome, usuário ou e-mail.",
        ),
    ]
    sort_by: UserSortField = UserSortField.ID
    sort_direction: SortDirection = SortDirection.ASC
    page: Annotated[int, Field(ge=MIN_PAGE)] = MIN_PAGE
    page_size: Annotated[int, Field(ge=MIN_PAGE_SIZE, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE

    def to_query(self) -> UserQuery:
        return UserQuery(
            search=self.search,
            sort_by=self.sort_by,
            sort_direction=self.sort_direction,
            page=self.page,
            page_size=self.page_size,
        )


class UserPageResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    items: list[UserPayload]
    page: int
    page_size: int
    total: int
    total_pages: int

    @classmethod
    def from_page(cls, page: Page[User]) -> "UserPageResponse":
        return cls(
            items=[UserPayload.from_domain(user) for user in page.items],
            page=page.page,
            page_size=page.page_size,
            total=page.total,
            total_pages=page.total_pages,
        )

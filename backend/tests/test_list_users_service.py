import pytest

from app.application.list_users import ListUsersService
from app.domain.pagination import SortDirection
from app.domain.queries import UserQuery, UserSortField
from app.domain.user import User
from app.persistence.memory_repository import InMemoryUserRepository

NAMES = ["Ana Souza", "Bruno Lima", "Carla Dias", "Diego Alves", "Ana Paula"]


@pytest.fixture
async def service() -> ListUsersService:
    repository = InMemoryUserRepository()
    for index, name in enumerate(NAMES, start=1):
        await repository.save(
            User(
                id=index,
                name=name,
                username=f"user{index}",
                email=f"user{index}@example.com",
                phone=f"1198765432{index}",
            )
        )
    return ListUsersService(repository)


async def test_paginates_on_the_server(service: ListUsersService) -> None:
    page = await service.execute(UserQuery(page=2, page_size=2))

    assert [user.id for user in page.items] == [3, 4]
    assert page.total == len(NAMES)
    assert page.total_pages == 3


async def test_filters_by_search_term(service: ListUsersService) -> None:
    page = await service.execute(UserQuery(search="ana"))

    assert [user.name for user in page.items] == ["Ana Souza", "Ana Paula"]
    assert page.total == 2


async def test_searches_by_id_and_email(service: ListUsersService) -> None:
    assert [user.id for user in (await service.execute(UserQuery(search="3"))).items] == [3]
    assert [user.id for user in (await service.execute(UserQuery(search="user4@"))).items] == [4]


async def test_searches_by_phone_ignoring_mask(service: ListUsersService) -> None:
    page = await service.execute(UserQuery(search="(11) 98765-4321"))

    assert [user.id for user in page.items] == [1]


async def test_term_with_letters_does_not_match_phone_digits(service: ListUsersService) -> None:
    page = await service.execute(UserQuery(search="user5"))

    assert [user.id for user in page.items] == [5]


async def test_sorts_by_column_and_direction(service: ListUsersService) -> None:
    page = await service.execute(
        UserQuery(sort_by=UserSortField.NAME, sort_direction=SortDirection.DESC)
    )

    assert page.items[0].name == "Diego Alves"


async def test_search_and_pagination_are_combined(service: ListUsersService) -> None:
    page = await service.execute(UserQuery(search="ana", page=2, page_size=1))

    assert [user.name for user in page.items] == ["Ana Paula"]
    assert page.total == 2
    assert page.total_pages == 2

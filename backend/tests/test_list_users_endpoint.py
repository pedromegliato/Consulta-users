from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.app import create_app
from app.api.dependencies import get_list_users_service
from app.application.list_users import ListUsersService
from app.persistence.memory_repository import InMemoryUserRepository
from tests.factories import build_user

ENDPOINT = "/api/users"


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    repository = InMemoryUserRepository()
    for user_id in range(1, 6):
        await repository.save(build_user(user_id))

    app = create_app()
    app.dependency_overrides[get_list_users_service] = lambda: ListUsersService(repository)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http_client:
        yield http_client


async def test_returns_requested_page(client: AsyncClient) -> None:
    response = await client.get(ENDPOINT, params={"page": 2, "page_size": 2})

    assert response.status_code == 200
    body = response.json()
    assert [item["id"] for item in body["items"]] == [3, 4]
    assert body["total"] == 5
    assert body["total_pages"] == 3


async def test_applies_search_and_sort(client: AsyncClient) -> None:
    response = await client.get(
        ENDPOINT, params={"search": "user5", "sort_by": "name", "sort_direction": "desc"}
    )

    body = response.json()
    assert [item["id"] for item in body["items"]] == [5]


async def test_rejects_invalid_pagination(client: AsyncClient) -> None:
    response = await client.get(ENDPOINT, params={"page": 0})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


async def test_rejects_unknown_sort_field(client: AsyncClient) -> None:
    response = await client.get(ENDPOINT, params={"sort_by": "senha"})

    assert response.status_code == 422

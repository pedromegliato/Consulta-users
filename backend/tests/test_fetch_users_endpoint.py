from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.app import create_app
from app.api.dependencies import get_fetch_users_service
from app.application.fetch_users import FetchUsersService
from app.domain.exceptions import ProviderTimeoutError
from tests.factories import build_user
from tests.fakes import FakeUserProvider

ENDPOINT = "/api/users/fetch"


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    app = create_app()
    provider = FakeUserProvider(
        {1: build_user(1), 2: build_user(2), 3: ProviderTimeoutError(3, "read timeout")}
    )
    app.dependency_overrides[get_fetch_users_service] = lambda: FetchUsersService(
        provider, max_concurrency=5
    )
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http_client:
        yield http_client


async def test_returns_users_and_failed_ids(client: AsyncClient) -> None:
    response = await client.post(ENDPOINT, json={"user_ids": [1, 2, 3, 4]})

    assert response.status_code == 200
    body = response.json()
    assert [user["id"] for user in body["users"]] == [1, 2]
    assert body["failed"] == [3, 4]


async def test_rejects_empty_id_list(client: AsyncClient) -> None:
    response = await client.post(ENDPOINT, json={"user_ids": []})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


async def test_rejects_non_positive_ids(client: AsyncClient) -> None:
    response = await client.post(ENDPOINT, json={"user_ids": [0, -1]})

    assert response.status_code == 422


async def test_rejects_payload_without_user_ids(client: AsyncClient) -> None:
    response = await client.post(ENDPOINT, json={})

    assert response.status_code == 422

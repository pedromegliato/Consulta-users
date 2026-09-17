import httpx
import pytest

from app.domain.exceptions import (
    InvalidProviderPayloadError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    UserNotFoundError,
)
from app.providers.http_user_provider import HttpUserProvider
from app.providers.retry import RetryPolicy

NO_WAIT_RETRY = RetryPolicy(attempts=3, base_delay_seconds=0.0, max_delay_seconds=0.0)

USER_PAYLOAD = {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "leanne@example.com",
    "phone": "1-770-736-8031",
}


def build_provider(handler) -> HttpUserProvider:
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="https://provider.test"
    )
    return HttpUserProvider(client, NO_WAIT_RETRY)


async def test_maps_provider_payload_to_domain_user() -> None:
    provider = build_provider(lambda request: httpx.Response(200, json=USER_PAYLOAD))

    user = await provider.get_user(1)

    assert user.id == 1
    assert user.name == "Leanne Graham"
    assert user.email == "leanne@example.com"


async def test_missing_user_raises_user_not_found() -> None:
    provider = build_provider(lambda request: httpx.Response(404))

    with pytest.raises(UserNotFoundError):
        await provider.get_user(99)


async def test_retries_on_429_and_succeeds() -> None:
    attempts = []

    def handler(request: httpx.Request) -> httpx.Response:
        attempts.append(request)
        if len(attempts) == 1:
            return httpx.Response(429, headers={"Retry-After": "0"})
        return httpx.Response(200, json=USER_PAYLOAD)

    user = await build_provider(handler).get_user(1)

    assert len(attempts) == 2
    assert user.id == 1


async def test_gives_up_after_exhausting_retries_on_server_error() -> None:
    attempts = []

    def handler(request: httpx.Request) -> httpx.Response:
        attempts.append(request)
        return httpx.Response(503)

    with pytest.raises(ProviderUnavailableError):
        await build_provider(handler).get_user(1)

    assert len(attempts) == NO_WAIT_RETRY.attempts


async def test_timeout_is_translated_to_provider_timeout() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out", request=request)

    with pytest.raises(ProviderTimeoutError):
        await build_provider(handler).get_user(1)


async def test_unexpected_payload_raises_invalid_provider_payload() -> None:
    provider = build_provider(lambda request: httpx.Response(200, json={"id": 1}))

    with pytest.raises(InvalidProviderPayloadError):
        await provider.get_user(1)

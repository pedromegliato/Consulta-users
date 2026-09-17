from app.application.fetch_users import FetchUsersService
from app.domain.exceptions import ProviderTimeoutError, ProviderUnavailableError, UserNotFoundError
from tests.factories import build_user
from tests.fakes import FakeUserProvider


async def test_returns_every_requested_user_on_success() -> None:
    users = {user_id: build_user(user_id) for user_id in (1, 2, 3)}
    service = FetchUsersService(FakeUserProvider(users), max_concurrency=5)

    result = await service.execute([1, 2, 3])

    assert [user.id for user in result.users] == [1, 2, 3]
    assert result.failed == []


async def test_failure_of_one_user_does_not_stop_the_others() -> None:
    provider = FakeUserProvider(
        {
            1: build_user(1),
            2: UserNotFoundError(2),
            3: build_user(3),
            4: ProviderTimeoutError(4, "read timeout"),
            5: ProviderUnavailableError(5, "status=503"),
        }
    )
    service = FetchUsersService(provider, max_concurrency=5)

    result = await service.execute([1, 2, 3, 4, 5])

    assert [user.id for user in result.users] == [1, 3]
    assert result.failed == [2, 4, 5]


async def test_unexpected_provider_exception_is_isolated() -> None:
    provider = FakeUserProvider({1: build_user(1), 2: RuntimeError("boom")})
    service = FetchUsersService(provider, max_concurrency=5)

    result = await service.execute([1, 2])

    assert [user.id for user in result.users] == [1]
    assert result.failed == [2]


async def test_repeated_ids_are_requested_once() -> None:
    provider = FakeUserProvider({1: build_user(1), 2: build_user(2)})
    service = FetchUsersService(provider, max_concurrency=5)

    result = await service.execute([1, 2, 1, 2, 1])

    assert provider.calls == [1, 2]
    assert [user.id for user in result.users] == [1, 2]


async def test_concurrency_never_exceeds_the_configured_limit() -> None:
    users = {user_id: build_user(user_id) for user_id in range(1, 11)}
    provider = FakeUserProvider(users, delay_seconds=0.01)
    service = FetchUsersService(provider, max_concurrency=3)

    result = await service.execute(list(users))

    assert provider.max_in_flight <= 3
    assert len(result.users) == 10

import pytest

from app.domain.exceptions import ProviderUnavailableError, UserNotFoundError
from app.providers.cached_user_provider import CachedUserProvider
from app.providers.mirroring_user_provider import MirroringUserProvider
from tests.factories import build_user
from tests.fakes import AlwaysFailingProvider, FakeUserCache, FakeUserProvider, FakeUserRepository


async def test_cache_avoids_a_second_call_to_the_delegate() -> None:
    delegate = FakeUserProvider({1: build_user(1)})
    provider = CachedUserProvider(FakeUserCache(), delegate)

    await provider.get_user(1)
    await provider.get_user(1)

    assert delegate.calls == [1]


async def test_mirror_serves_the_user_when_the_delegate_is_unavailable() -> None:
    repository = FakeUserRepository({7: build_user(7)})
    delegate = AlwaysFailingProvider(ProviderUnavailableError(7, "status=503"))
    provider = MirroringUserProvider(repository, delegate)

    user = await provider.get_user(7)

    assert user.id == 7


async def test_mirror_does_not_mask_a_missing_user() -> None:
    repository = FakeUserRepository()
    delegate = AlwaysFailingProvider(UserNotFoundError(7))
    provider = MirroringUserProvider(repository, delegate)

    with pytest.raises(UserNotFoundError):
        await provider.get_user(7)


async def test_resolved_user_is_persisted_in_the_mirror() -> None:
    repository = FakeUserRepository()
    provider = MirroringUserProvider(repository, FakeUserProvider({3: build_user(3)}))

    await provider.get_user(3)

    assert repository.stored[3].id == 3

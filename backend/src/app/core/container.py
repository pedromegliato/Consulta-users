from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass

import httpx
from redis.asyncio import Redis

from app.application.fetch_users import FetchUsersService
from app.application.list_users import ListUsersService
from app.cache.memory import InMemoryUserCache
from app.cache.redis_cache import RedisUserCache
from app.core.config import Settings
from app.domain.ports import UserCache, UserProvider, UserStore
from app.persistence.database import create_engine, create_schema, create_session_factory
from app.persistence.memory_repository import InMemoryUserRepository
from app.persistence.user_repository import PostgresUserRepository
from app.providers.cached_user_provider import CachedUserProvider
from app.providers.http_user_provider import HttpUserProvider
from app.providers.mirroring_user_provider import MirroringUserProvider
from app.providers.retry import RetryPolicy


@dataclass(frozen=True)
class Services:
    fetch_users: FetchUsersService
    list_users: ListUsersService


@asynccontextmanager
async def build_services(settings: Settings) -> AsyncIterator[Services]:
    async with AsyncExitStack() as stack:
        client = await stack.enter_async_context(_http_client(settings))
        cache = await stack.enter_async_context(_user_cache(settings))
        store = await stack.enter_async_context(_user_store(settings))

        provider = _build_provider(client, cache, store, settings)
        yield Services(
            fetch_users=FetchUsersService(provider, settings.max_concurrency),
            list_users=ListUsersService(store),
        )


def _build_provider(
    client: httpx.AsyncClient,
    cache: UserCache,
    store: UserStore,
    settings: Settings,
) -> UserProvider:
    http_provider = HttpUserProvider(
        client,
        RetryPolicy(
            attempts=settings.retry_attempts,
            base_delay_seconds=settings.retry_base_delay_seconds,
            max_delay_seconds=settings.retry_max_delay_seconds,
        ),
    )
    return CachedUserProvider(cache, MirroringUserProvider(store, http_provider))


@asynccontextmanager
async def _http_client(settings: Settings) -> AsyncIterator[httpx.AsyncClient]:
    limits = httpx.Limits(max_connections=settings.max_concurrency * 2)
    async with httpx.AsyncClient(
        base_url=settings.provider_base_url,
        timeout=settings.provider_timeout_seconds,
        limits=limits,
    ) as client:
        yield client


@asynccontextmanager
async def _user_cache(settings: Settings) -> AsyncIterator[UserCache]:
    if settings.redis_url is None:
        yield InMemoryUserCache(settings.cache_ttl_seconds)
        return

    client: Redis = Redis.from_url(settings.redis_url, decode_responses=True)
    try:
        yield RedisUserCache(client, settings.cache_ttl_seconds)
    finally:
        await client.aclose()


@asynccontextmanager
async def _user_store(settings: Settings) -> AsyncIterator[UserStore]:
    if settings.database_url is None:
        yield InMemoryUserRepository()
        return

    engine = create_engine(settings.database_url)
    try:
        await create_schema(engine)
        yield PostgresUserRepository(create_session_factory(engine))
    finally:
        await engine.dispose()

import asyncio
import logging
import time
from collections.abc import Sequence
from dataclasses import dataclass

from app.domain.exceptions import ProviderError
from app.domain.ports import UserProvider
from app.domain.user import User

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class FetchUsersResult:
    users: list[User]
    failed: list[int]


class FetchUsersService:
    def __init__(self, provider: UserProvider, max_concurrency: int) -> None:
        self._provider = provider
        self._max_concurrency = max_concurrency

    async def execute(self, user_ids: Sequence[int]) -> FetchUsersResult:
        requested = list(dict.fromkeys(user_ids))
        semaphore = asyncio.Semaphore(self._max_concurrency)
        started_at = time.perf_counter()

        resolved = await asyncio.gather(
            *(self._resolve(user_id, semaphore) for user_id in requested)
        )
        result = FetchUsersResult(
            users=[user for user in resolved if user is not None],
            failed=[
                user_id for user_id, user in zip(requested, resolved, strict=True) if user is None
            ],
        )

        logger.info(
            "fetch_users_completed",
            extra={
                "requested": len(requested),
                "resolved": len(result.users),
                "failed": len(result.failed),
                "failed_ids": result.failed,
                "duration_ms": round((time.perf_counter() - started_at) * 1000, 2),
            },
        )
        return result

    async def _resolve(self, user_id: int, semaphore: asyncio.Semaphore) -> User | None:
        async with semaphore:
            return await self._resolve_isolated(user_id)

    async def _resolve_isolated(self, user_id: int) -> User | None:
        try:
            return await self._provider.get_user(user_id)
        except ProviderError as error:
            logger.warning(
                "user_fetch_failed",
                extra={"user_id": user_id, "reason": error.reason, "detail": error.detail},
            )
        except Exception:
            logger.exception("user_fetch_unexpected_error", extra={"user_id": user_id})
        return None

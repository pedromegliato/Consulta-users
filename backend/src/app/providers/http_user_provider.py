import asyncio
import logging
import time

import httpx

from app.domain.exceptions import (
    InvalidProviderPayloadError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    UserNotFoundError,
)
from app.domain.user import User
from app.providers.retry import RetryPolicy
from app.providers.schemas import ProviderUserPayload

logger = logging.getLogger(__name__)

RETRYABLE_STATUSES = frozenset({429, 500, 502, 503, 504})


class HttpUserProvider:
    """Adapter HTTP do provider externo, com retry para 429/5xx e timeout."""

    def __init__(self, client: httpx.AsyncClient, retry_policy: RetryPolicy) -> None:
        self._client = client
        self._retry_policy = retry_policy

    async def get_user(self, user_id: int) -> User:
        response = await self._get_with_retry(user_id)
        if response.status_code == httpx.codes.NOT_FOUND:
            raise UserNotFoundError(user_id)
        if response.is_error:
            raise ProviderUnavailableError(user_id, f"status={response.status_code}")
        return self._to_user(user_id, response)

    async def _get_with_retry(self, user_id: int) -> httpx.Response:
        attempt = 1
        while True:
            is_last_attempt = attempt >= self._retry_policy.attempts
            try:
                response = await self._request(user_id, attempt)
            except ProviderTimeoutError:
                if is_last_attempt:
                    raise
                delay = self._retry_policy.delay_for(attempt)
                reason = "timeout"
            else:
                if is_last_attempt or response.status_code not in RETRYABLE_STATUSES:
                    return response
                delay = self._retry_policy.delay_for(attempt, _retry_after_seconds(response))
                reason = f"status={response.status_code}"

            logger.info(
                "provider_retry_scheduled",
                extra={"user_id": user_id, "attempt": attempt, "reason": reason, "delay": delay},
            )
            await asyncio.sleep(delay)
            attempt += 1

    async def _request(self, user_id: int, attempt: int) -> httpx.Response:
        started_at = time.perf_counter()
        try:
            response = await self._client.get(f"/users/{user_id}")
        except httpx.TimeoutException as error:
            raise ProviderTimeoutError(user_id, str(error)) from error
        except httpx.HTTPError as error:
            raise ProviderUnavailableError(user_id, str(error)) from error

        logger.debug(
            "provider_request",
            extra={
                "user_id": user_id,
                "attempt": attempt,
                "status_code": response.status_code,
                "duration_ms": round((time.perf_counter() - started_at) * 1000, 2),
            },
        )
        return response

    @staticmethod
    def _to_user(user_id: int, response: httpx.Response) -> User:
        try:
            return ProviderUserPayload.model_validate(response.json()).to_domain()
        except (ValueError, TypeError) as error:
            raise InvalidProviderPayloadError(user_id, repr(error)) from error


def _retry_after_seconds(response: httpx.Response) -> float | None:
    header = response.headers.get("Retry-After")
    if header is None:
        return None
    try:
        return float(header)
    except ValueError:
        return None

import logging
import time

from app.domain.pagination import Page
from app.domain.ports import UserQueryRepository
from app.domain.queries import UserQuery
from app.domain.user import User

logger = logging.getLogger(__name__)


class ListUsersService:
    def __init__(self, repository: UserQueryRepository) -> None:
        self._repository = repository

    async def execute(self, query: UserQuery) -> Page[User]:
        started_at = time.perf_counter()
        page = await self._repository.search(query)

        logger.info(
            "list_users_completed",
            extra={
                "search": query.search,
                "sort_by": query.sort_by.value,
                "sort_direction": query.sort_direction.value,
                "page": query.page,
                "page_size": query.page_size,
                "total": page.total,
                "duration_ms": round((time.perf_counter() - started_at) * 1000, 2),
            },
        )
        return page

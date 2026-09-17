import logging

from app.domain.exceptions import ProviderError, UserNotFoundError
from app.domain.ports import UserProvider, UserRepository
from app.domain.user import User

logger = logging.getLogger(__name__)


class MirroringUserProvider:
    """Decorator de resiliencia: espelha o que foi resolvido e serve o espelho quando o
    provider esta indisponivel. Usuario inexistente nao e degradavel e propaga direto."""

    def __init__(self, repository: UserRepository, delegate: UserProvider) -> None:
        self._repository = repository
        self._delegate = delegate

    async def get_user(self, user_id: int) -> User:
        try:
            user = await self._delegate.get_user(user_id)
        except UserNotFoundError:
            raise
        except ProviderError as error:
            mirrored = await self._repository.find(user_id)
            if mirrored is None:
                raise
            logger.info(
                "mirror_fallback_used",
                extra={"user_id": user_id, "reason": error.reason},
            )
            return mirrored

        await self._repository.save(user)
        return user

class ProviderError(Exception):
    """Falha ao resolver um usuario em uma fonte externa."""

    reason = "provider_error"

    def __init__(self, user_id: int, detail: str = "") -> None:
        super().__init__(detail or self.reason)
        self.user_id = user_id
        self.detail = detail


class UserNotFoundError(ProviderError):
    reason = "not_found"


class ProviderTimeoutError(ProviderError):
    reason = "timeout"


class ProviderUnavailableError(ProviderError):
    reason = "provider_unavailable"


class InvalidProviderPayloadError(ProviderError):
    reason = "invalid_payload"

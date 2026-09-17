import logging
import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.context import request_id

logger = logging.getLogger(__name__)

REQUEST_ID_HEADER = "X-Request-ID"


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Correlaciona logs por requisicao e registra o acesso em formato estruturado."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        current_id = request.headers.get(REQUEST_ID_HEADER) or uuid4().hex
        token = request_id.set(current_id)
        started_at = time.perf_counter()
        try:
            response = await call_next(request)
        finally:
            request_id.reset(token)

        response.headers[REQUEST_ID_HEADER] = current_id
        logger.info(
            "http_request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round((time.perf_counter() - started_at) * 1000, 2),
                "request_id": current_id,
            },
        )
        return response

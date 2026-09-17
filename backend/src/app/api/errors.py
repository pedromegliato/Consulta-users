import logging
from typing import cast

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import ExceptionHandler

from app.api.error_catalog import (
    INTERNAL_ERROR,
    VALIDATION_ERROR,
    ErrorDefinition,
    definition_for_status,
)
from app.api.schemas.errors import ErrorBody, ErrorResponse
from app.core.context import request_id

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, cast(ExceptionHandler, _handle_validation))
    app.add_exception_handler(StarletteHTTPException, cast(ExceptionHandler, _handle_http_error))
    app.add_exception_handler(Exception, cast(ExceptionHandler, _handle_unexpected))


async def _handle_validation(_: Request, exception: RequestValidationError) -> JSONResponse:
    details = [
        f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}"
        for error in exception.errors()
    ]
    logger.info("request_rejected", extra={"code": VALIDATION_ERROR.code, "details": details})
    return _error_response(VALIDATION_ERROR, details)


async def _handle_http_error(_: Request, exception: StarletteHTTPException) -> JSONResponse:
    definition = definition_for_status(exception.status_code)
    logger.info(
        "request_failed",
        extra={"code": definition.code, "status_code": exception.status_code},
    )
    return _error_response(definition)


async def _handle_unexpected(_: Request, exception: Exception) -> JSONResponse:
    logger.exception("unhandled_error", extra={"code": INTERNAL_ERROR.code})
    return _error_response(INTERNAL_ERROR)


def _error_response(definition: ErrorDefinition, details: list[str] | None = None) -> JSONResponse:
    body = ErrorResponse(
        error=ErrorBody(
            code=definition.code,
            message=definition.message,
            details=details or [],
            request_id=request_id.get(),
        )
    )
    return JSONResponse(status_code=definition.status_code, content=body.model_dump())

import logging
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions.base import ApiException

logger = logging.getLogger("api")

async def api_exception_handler(
    request: Request,
    exc: ApiException,
) -> JSONResponse:
    """
    Базовый хэндлер для всех ошибок типа "ApiException errors".
    """

    # Логируем
    if exc.status_code >= 500:
        logger.exception(
            "Internal error",
            extra={
                "path": request.url.path,
                "error_code": exc.error_code,
                "detail": exc.detail,
            },
        )
    else:
        logger.warning(
            "Client error",
            extra={
                "path": request.url.path,
                "error_code": exc.error_code,
                "detail": exc.detail,
            },
        )

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
        headers=exc.headers,
    )

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Базовый хэндлер для всех ошибок типа "RequestValidationError".
    """
    logger.warning(
        "Validation error",
        extra={
            "path": request.url.path,
            "method": request.method,
            "errors": exc.errors(),
            "body": exc.body,
        },
    )

    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception("Unhandled exception")

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

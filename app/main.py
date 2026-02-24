from contextlib import asynccontextmanager

from fastapi.exceptions import RequestValidationError
import uvicorn
from fastapi import FastAPI

from app.api.api_v1.exception_handlers import api_exception_handler, unhandled_exception_handler, validation_exception_handler
from app.core.exceptions.base import ApiException

from .core.config import settings
from .core.db import db_session
from .core.logging import setup_logging
from typing import cast
from starlette.types import ExceptionHandler

from .api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    try:
        yield
    finally:
        await db_session.dispose()


app = FastAPI(
    lifespan=lifespan,
    log_level="info",
)

app.add_exception_handler(ApiException, cast(ExceptionHandler, api_exception_handler))
app.add_exception_handler(Exception, cast(ExceptionHandler, unhandled_exception_handler))
app.add_exception_handler(RequestValidationError, cast(ExceptionHandler, validation_exception_handler))

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.run.host, port=settings.run.port, reload=True)

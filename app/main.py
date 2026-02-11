from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from .core.config import settings
from .core.db import db_session
from .core.logging import setup_logging
from .core.models import Base

# from .api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    async with db_session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await db_session.dispose()


app = FastAPI(
    lifespan=lifespan,
    log_level="info",
)

# app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.run.host, port=settings.run.port, reload=True)

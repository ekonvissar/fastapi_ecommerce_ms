from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.session import async_engine
from app.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await async_engine.dispose()
    await redis_client.aclose()
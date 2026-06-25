from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.session import async_engine



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await async_engine.dispose()
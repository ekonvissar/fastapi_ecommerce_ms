from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.routers import auth, catalog, checkout, health

API_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(timeout=30.0)
    yield
    await app.state.http.aclose()


app = FastAPI(
    title="Ecommerce BFF",
    version="0.1.0",
    lifespan=lifespan,
    docs_url=f"{API_PREFIX}/docs",
    openapi_url=f"{API_PREFIX}/openapi.json",
)

app.include_router(health.router, prefix=API_PREFIX)
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(catalog.router, prefix=API_PREFIX)
app.include_router(checkout.router, prefix=API_PREFIX)

from pathlib import Path

from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from app.api.categories_router import category_router
from app.api.products_router import product_router
from app.api.reviews_router import review_router
from app.exceptions import CatalogError
from app.lifespan import lifespan

MEDIA_DIR = Path("../media")

app = FastAPI(title="Catalog Service", version="0.1.0", lifespan=lifespan)

app.include_router(category_router)
app.include_router(product_router)
app.include_router(review_router)

async def catalog_error_handler(_request, exc: CatalogError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")
app.add_exception_handler(CatalogError, catalog_error_handler)
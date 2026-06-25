from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.api.router import router
from app.exceptions import IdentityError
from app.lifespan import lifespan


app = FastAPI(title="Identity Service", version="0.1.0", lifespan=lifespan)
app.include_router(router)

async def identity_error_handler(_request, exc: IdentityError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )
app.add_exception_handler(IdentityError, identity_error_handler)

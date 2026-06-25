from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.config import Settings, get_settings
from app.deps import get_http_client
from app.proxy import CATALOG_RESOURCES, forward_request

router = APIRouter(tags=["catalog"])

PROXY_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]


@router.api_route(
    "/{resource}",
    methods=PROXY_METHODS,
    include_in_schema=True,
)
@router.api_route(
    "/{resource}/",
    methods=PROXY_METHODS,
    include_in_schema=True,
)
@router.api_route(
    "/{resource}/{path:path}",
    methods=PROXY_METHODS,
    include_in_schema=True,
)
async def proxy_catalog(
    request: Request,
    resource: str,
    path: str = "",
    http=Depends(get_http_client),
    settings: Settings = Depends(get_settings),
):
    if resource not in CATALOG_RESOURCES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )

    upstream_path = resource if not path else f"{resource}/{path}"
    if request.url.path.endswith("/") and not upstream_path.endswith("/"):
        upstream_path += "/"

    return await forward_request(
        request,
        http,
        settings.catalog_url,
        upstream_path,
    )

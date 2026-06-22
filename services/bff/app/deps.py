import httpx
from fastapi import Depends, Request

from app.clients.identity import IdentityClient
from app.config import Settings, get_settings


def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http


def get_settings_dep() -> Settings:
    return get_settings()


def get_identity_client(
    request: Request,
    settings: Settings = Depends(get_settings_dep),
) -> IdentityClient:
    return IdentityClient(request.app.state.http, settings)

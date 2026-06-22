from contextlib import asynccontextmanager

import httpx
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.clients.identity import IdentityClient
from app.config import Settings, get_settings
from app.deps import get_identity_client
from app.proxy import proxy_response
from app.schemas.user import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
async def register(
    user: UserCreate,
    identity: IdentityClient = Depends(get_identity_client),
    settings: Settings = Depends(get_settings),
):
    upstream = await identity.register(user.model_dump())
    return proxy_response(
        upstream.status_code,
        upstream.content,
        dict(upstream.headers),
        cookie_path=settings.auth_cookie_path if upstream.status_code < 400 else None,
    )


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    identity: IdentityClient = Depends(get_identity_client),
    settings: Settings = Depends(get_settings),
):
    upstream = await identity.login(form_data.username, form_data.password)
    return proxy_response(
        upstream.status_code,
        upstream.content,
        dict(upstream.headers),
        cookie_path=settings.auth_cookie_path,
    )


@router.post("/refresh")
async def refresh(
    request: Request,
    identity: IdentityClient = Depends(get_identity_client),
    settings: Settings = Depends(get_settings),
):
    upstream = await identity.refresh(request.cookies.get("refresh_token"))
    return proxy_response(
        upstream.status_code,
        upstream.content,
        dict(upstream.headers),
        cookie_path=settings.auth_cookie_path,
    )


@router.post("/logout")
async def logout(
    request: Request,
    identity: IdentityClient = Depends(get_identity_client),
    settings: Settings = Depends(get_settings),
):
    upstream = await identity.logout(request.cookies.get("refresh_token"))
    return proxy_response(
        upstream.status_code,
        upstream.content,
        dict(upstream.headers),
        cookie_path=settings.auth_cookie_path,
    )

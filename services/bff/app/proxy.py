import httpx
from fastapi import Request
from starlette.responses import Response

HOP_BY_HOP_HEADERS = frozenset(
    {
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailers",
        "transfer-encoding",
        "upgrade",
        "host",
        "content-length",
    }
)

CATALOG_RESOURCES = frozenset({"categories", "products", "reviews"})


def filtered_request_headers(request: Request) -> dict[str, str]:
    return {
        name: value
        for name, value in request.headers.items()
        if name.lower() not in HOP_BY_HOP_HEADERS
    }


async def forward_request(
    request: Request,
    http: httpx.AsyncClient,
    base_url: str,
    path: str,
) -> Response:
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    if request.url.query:
        url = f"{url}?{request.url.query}"

    upstream = await http.request(
        method=request.method,
        url=url,
        headers=filtered_request_headers(request),
        content=await request.body(),
    )
    return proxy_response(
        upstream.status_code,
        upstream.content,
        dict(upstream.headers),
    )


def rewrite_set_cookie_path(raw_cookie: str, new_path: str) -> str:
    if "Path=" not in raw_cookie:
        return f"{raw_cookie}; Path={new_path}"
    parts = raw_cookie.split(";")
    rebuilt: list[str] = []
    path_set = False
    for part in parts:
        stripped = part.strip()
        if stripped.lower().startswith("path="):
            rebuilt.append(f"Path={new_path}")
            path_set = True
        else:
            rebuilt.append(stripped)
    if not path_set:
        rebuilt.append(f"Path={new_path}")
    return "; ".join(rebuilt)


def proxy_response(
    status_code: int,
    content: bytes,
    headers: dict[str, str],
    *,
    cookie_path: str | None = None,
) -> Response:
    response_headers: dict[str, str] = {}
    set_cookies: list[str] = []

    for key, value in headers.items():
        lower = key.lower()
        if lower == "set-cookie":
            set_cookies.append(
                rewrite_set_cookie_path(value, cookie_path) if cookie_path else value
            )
        elif lower in {"content-length", "transfer-encoding", "connection"}:
            continue
        else:
            response_headers[key] = value

    response = Response(
        content=content,
        status_code=status_code,
        headers=response_headers,
        media_type=headers.get("content-type"),
    )
    for cookie in set_cookies:
        response.headers.append("set-cookie", cookie)
    return response

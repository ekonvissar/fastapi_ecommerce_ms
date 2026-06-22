from starlette.responses import Response


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

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.config import Settings, get_settings
from app.deps import get_http_client

router = APIRouter(prefix="/checkout", tags=["checkout"])


@router.get("/")
async def checkout_preview(
    request: Request,
    http=Depends(get_http_client),
    settings: Settings = Depends(get_settings),
) -> dict:
    """Пример оркестрации: корзина + каталог → один ответ клиенту.

    Сейчас catalog/ordering ещё не подняты — показываем структуру вызовов.
    """
    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
        )

    headers = {"Authorization": auth}

    cart_resp = await http.get(f"{settings.ordering_url}/cart/", headers=headers)
    if cart_resp.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ordering service is not available yet",
        )
    if cart_resp.status_code >= 400:
        raise HTTPException(
            status_code=cart_resp.status_code,
            detail=cart_resp.json().get("detail", "Cart request failed"),
        )

    cart_items = cart_resp.json()
    if not cart_items:
        return {"items": [], "total": "0.00"}

    enriched_items = []
    total = 0.0

    for item in cart_items:
        product_id = item["product_id"]
        product_resp = await http.get(
            f"{settings.catalog_url}/products/{product_id}",
            headers=headers,
        )
        if product_resp.status_code >= 400:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Catalog lookup failed for product {product_id}",
            )
        product = product_resp.json()
        line_total = float(product["price"]) * item["quantity"]
        total += line_total
        enriched_items.append(
            {
                "product_id": product_id,
                "name": product["name"],
                "price": product["price"],
                "quantity": item["quantity"],
                "line_total": f"{line_total:.2f}",
            }
        )

    return {"items": enriched_items, "total": f"{total:.2f}"}

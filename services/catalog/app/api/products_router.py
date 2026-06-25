from typing import Annotated

from fastapi import APIRouter, Depends, File, Query, UploadFile, status

from app.auth import get_current_seller, TokenUserData
from app.deps import get_product_service, get_review_service
from app.repositories.product_repository import ProductListFilters
from app.schemas.product import ProductCreate, ProductList
from app.schemas.review import Review as ReviewSchema
from app.services.product_service import ProductService
from app.services.review_service import ReviewService
from app.schemas.product import Product as ProductSchema

product_router = APIRouter(prefix="/products", tags=["products"])

product_reviews_router = APIRouter(prefix="/{product_id}/reviews")


@product_router.get("/", response_model=ProductList)
async def get_all_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: int | None = Query(None, description="ID категории для фильтрации"),
    search: str | None = Query(
        None, min_length=1, description="Поиск по названию/описанию"
    ),
    min_price: float | None = Query(None, ge=0, description="Минимальная цена товара"),
    max_price: float | None = Query(None, ge=0, description="Максимальная цена товара"),
    in_stock: bool | None = Query(
        None, description="true — только товары в наличии, false — только без остатка"
    ),
    seller_id: int | None = Query(None, description="ID продавца для фильтрации"),
    service: ProductService = Depends(get_product_service),
):
    filters = ProductListFilters(
        page=page,
        page_size=page_size,
        category_id=category_id,
        search=search,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        seller_id=seller_id,
    )
    items, total = await service.list_products(filters)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@product_router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate = Depends(ProductCreate.as_form),
    image: Annotated[UploadFile | None, File()] = None,
    current_user: TokenUserData = Depends(get_current_seller),
    service: ProductService = Depends(get_product_service),
):
    return await service.create(product, current_user["id"], image)


@product_router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    return await service.get_product(product_id)


@product_router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int,
    product: ProductCreate = Depends(ProductCreate.as_form),
    image: UploadFile | None = File(None),
    current_user: TokenUserData = Depends(get_current_seller),
    service: ProductService = Depends(get_product_service),
):
    return await service.update(product_id, product, current_user["id"], image)


@product_router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(
    product_id: int,
    current_user: TokenUserData = Depends(get_current_seller),
    service: ProductService = Depends(get_product_service),
):
    return await service.delete(product_id, current_user["id"])


@product_reviews_router.get("/", response_model=list[ReviewSchema])
async def get_reviews_by_product(
    product_id: int,
    service: ReviewService = Depends(get_review_service),
):
    return await service.list_by_product(product_id)


product_router.include_router(product_reviews_router)

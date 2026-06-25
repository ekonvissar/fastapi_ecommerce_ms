from fastapi import APIRouter, Depends, status

from app.deps import get_category_service, get_product_service
from app.schemas.category import Category as CategorySchema
from app.schemas.category import CategoryCreate
from app.services.category_service import CategoryService
from app.services.product_service import ProductService
from app.schemas.product import Product as ProductSchema

category_router = APIRouter(prefix="/categories", tags=["categories"])

category_products_router = APIRouter(prefix="/{category_id}/products")


@category_router.get("/", response_model=list[CategorySchema])
async def get_categories(service: CategoryService = Depends(get_category_service)):
    return await service.list_categories()


@category_router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    return await service.create(category)


@category_router.put("/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: int,
    category: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    return await service.update(category_id, category)


@category_router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
):
    return await service.delete(category_id)


@category_products_router.get("/", response_model=list[ProductSchema])
async def get_products_by_category(
    category_id: int,
    service: ProductService = Depends(get_product_service),
):
    return await service.list_by_category(category_id)


category_router.include_router(category_products_router)

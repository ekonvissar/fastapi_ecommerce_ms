from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.review_repository import ReviewRepository
from app.services.category_service import CategoryService
from app.services.image_storage import ImageStorage
from app.services.product_service import ProductService
from app.services.review_service import ReviewService
from app.db.deps import get_async_db

_image_storage = ImageStorage()


def get_category_repository(
    db: AsyncSession = Depends(get_async_db),
) -> CategoryRepository:
    return CategoryRepository(db)


def get_product_repository(
    db: AsyncSession = Depends(get_async_db),
) -> ProductRepository:
    return ProductRepository(db)


def get_review_repository(
    db: AsyncSession = Depends(get_async_db),
) -> ReviewRepository:
    return ReviewRepository(db)


def get_image_storage() -> ImageStorage:
    return _image_storage


def get_category_service(
    categories: CategoryRepository = Depends(get_category_repository),
) -> CategoryService:
    return CategoryService(categories)


def get_product_service(
    products: ProductRepository = Depends(get_product_repository),
    categories: CategoryRepository = Depends(get_category_repository),
    images: ImageStorage = Depends(get_image_storage),
) -> ProductService:
    return ProductService(products, categories, images)


def get_review_service(
    reviews: ReviewRepository = Depends(get_review_repository),
    products: ProductRepository = Depends(get_product_repository),
) -> ReviewService:
    return ReviewService(reviews, products)

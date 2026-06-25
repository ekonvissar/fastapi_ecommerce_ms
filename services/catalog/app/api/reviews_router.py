from fastapi import APIRouter, Depends, status

from app.auth import get_current_admin, get_current_buyer, TokenUserData
from app.deps import get_review_service
from app.schemas.review import Review as ReviewSchema
from app.schemas.review import ReviewCreate
from app.services.review_service import ReviewService

review_router = APIRouter(prefix="/reviews", tags=["reviews"])


@review_router.get("/", response_model=list[ReviewSchema])
async def get_reviews(service: ReviewService = Depends(get_review_service)):
    return await service.list_reviews()


@review_router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    current_user: TokenUserData = Depends(get_current_buyer),
    service: ReviewService = Depends(get_review_service),
):
    return await service.create(review, current_user["id"])


@review_router.delete("/{review_id}", status_code=status.HTTP_200_OK)
async def delete_review(
    review_id: int,
    current_user: TokenUserData = Depends(get_current_admin),
    service: ReviewService = Depends(get_review_service),
):
    return await service.delete(review_id)

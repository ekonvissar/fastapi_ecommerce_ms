from pydantic import BaseModel, ConfigDict, Field, EmailStr


class CategoryBrief(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ProductBrief(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class UserPublic(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class PaginationResponse[T](BaseModel):
    items: list[T] = Field(..., description="Элементы текущей страницы")
    total: int = Field(ge=0, description="Общее количество")
    page: int = Field(ge=1, description="Текущая страница")
    page_size: int = Field(ge=1, description="Размер страницы")

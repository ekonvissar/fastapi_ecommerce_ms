from typing import Annotated

from fastapi import Depends, Request
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: Annotated[EmailStr, Field(description="Email пользователя")]
    password: Annotated[str, Field(min_length=8)]
    role: Annotated[str, Field(default="buyer", pattern="^(buyer|seller|admin)$")]


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str

    model_config = ConfigDict(from_attributes=True)

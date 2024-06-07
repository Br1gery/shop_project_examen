from pydantic import BaseModel, Field, EmailStr
from typing import List
from datetime import date,datetime

class UserCreate(BaseModel):
    username: str = Field(..., max_length=255, example='UserName')
    password: str = Field(max_length=255, example='UserName')

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str = Field(..., max_length=255, example='UserName')
    password: str = Field(max_length=255, example='UserName')

    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    name: str = Field(...,example = 'example_name')
    description: str = Field(..., example = 'example_description')

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str = Field(...,example='example_name')
    description: str = Field(..., example = 'example_description')
    price: int = Field(...,gt = 0, example = 100)
    avg_rating: float = Field(None, ge = 0, example = 0)

    category_ids: List[int] = None

    class Config:
        orm_mode = True

class ReviewCreate(BaseModel):
    rating: int = Field(...,gt=0,le=5,example = 0)
    body: str = Field(...,example='example_review_body')

    product_id: int = Field(...,gt = 0,example = 1)

    class Config:
        orm_mode = True
from pydantic import BaseModel,Field
from datetime import datetime
from typing import List

class CategoryBase(BaseModel):
    id: int = Field(None,gt=0, example= 1)
    name: str = Field(...,example = 'example_name')
    description: str = Field(..., example = 'example_description')

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    id: int = Field(None, gt=0, example = 1)
    name: str = Field(...,example='example_name')
    description: str = Field(..., example = 'example_description')
    price: int = Field(...,gt = 0, example = 100)
    avg_rating: int = Field(...,gt = 0, example = 0)

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    id: int = Field(None,gt=0,example = 1)
    rating: int = Field(...,gt=0,le=5,example = 0)
    body: str = Field(...,example='example_review_body')
    

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    id: int = Field(None, gt=0, example=1)
    username: str = Field(..., max_length=255, example='example_username')

    class Config:
        orm_mode = True

class UserBaseReg(BaseModel):
    id: int = Field(None, gt=0, example=1)
    username: str = Field(..., max_length=255, example='example_username')
    password: str = Field(...,example = 'eaxmple_pass')

    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    id: int = Field(None, gt=0, example=1)
    name: str = Field(...,example = 'User')
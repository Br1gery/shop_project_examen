from .base_models import *
from typing import List

class ReviewSchema(ReviewBase):
    user: UserBase

class ProductSchema(ProductBase):
    categories: List[CategoryBase]
    reviews: List[ReviewSchema]

class UserSchema(UserBase):
    role: RoleBase
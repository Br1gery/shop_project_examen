from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
from auth import AuthHandler

auth_handler = AuthHandler()

router = APIRouter(
    prefix="/product",
    tags=["product"],
)

@router.get("/", response_model=List[pyd.ProductSchema])
async def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


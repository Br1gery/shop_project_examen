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

@router.post('/add_product',response_model=pyd.ProductSchema)
async def add_product(prod_input:pyd.ProductCreate,username=Depends(auth_handler.auth_wrapper), db:Session=Depends(get_db)):
    user_db = db.query(models.User).filter(
        models.User.username == username
    ).first()
    if user_db.role_id == 1:
        raise HTTPException(401,'Нет прав')

    prod_db = db.query(models.Product).filter(
        models.Category.name == prod_input.name
    ).first()
    if prod_db:
        raise HTTPException(400,detail='Product exists')
    prod_db = models.Product()
    prod_db.name = prod_input.name
    prod_db.description = prod_input.description
    prod_db.price = prod_input.price
    prod_db.avg_rating = 0
 
    for category_id in prod_input.category_ids:
        category_db = db.query(models.Category).filter(
            models.Category.id==category_id
        ).first()
        if category_db:
            prod_db.categories.append(category_db)
        else:
            raise HTTPException(404,"Category not found")
        
    db.add(prod_db)
    db.commit()
    return prod_db

@router.put('/{product_id}',response_model=pyd.ProductCreate)
async def change_category(prod_input:pyd.ProductCreate,product_id:int,username=Depends(auth_handler.auth_wrapper),db:Session = Depends(get_db)):
    user_db = db.query(models.User).filter(
        models.User.username == username
    ).first()
    if user_db.role_id == 1:
        raise HTTPException(401,'Нет прав')

    prod_db = db.query(models.Product).filter(
        models.Product.name == prod_input.name
    ).first()
    if prod_db:
        raise HTTPException(400,detail='Product exists')
    prod_db = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()
    prod_db.name = prod_input.name
    prod_db.description = prod_input.description
    prod_db.price = prod_input.price
    prod_db.avg_rating = 0

    for category_id in prod_input.category_ids:
        category_db = db.query(models.Category).filter(
            models.Category.id==category_id
        ).first()
        if category_db:
            prod_db.categories.clear()
            prod_db.categories.append(category_db)
        else:
            raise HTTPException(404,"Category not found")
        
    db.commit()
    return prod_db
    
@router.delete('/delete/{product_id}')
async def delete_product(product_id:int,username = Depends(auth_handler.auth_wrapper),db:Session=Depends(get_db)):
    user_db = db.query(models.User).filter(
        models.User.username == username
    ).first()
    if user_db.role_id == 1:
        raise HTTPException(401,'Нет прав')
    
    prod_db = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()
    if not prod_db:
        raise HTTPException(403,detail='Product not found')
    db.query(models.Review).filter(models.Review.product_id==product_id).delete()
    db.delete(prod_db)
    db.commit()
    return 'success'
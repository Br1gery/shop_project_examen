from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
from auth import AuthHandler
auth_handler = AuthHandler()


router = APIRouter(
    prefix="/category",
    tags=["category"],
)


@router.get('/',response_model=List[pyd.CategoryBase])
async def get_categories(db:Session=Depends(get_db)):
    cat_db = db.query(models.Category).all()
    return cat_db

@router.post('/add_category',response_model=pyd.CategoryCreate)
async def add_category(cat_input:pyd.CategoryCreate,username=Depends(auth_handler.auth_wrapper), db:Session=Depends(get_db)):
    user_db = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if user_db.role_id == 1:
        raise HTTPException(401,'Нет прав')

    cat_db = db.query(models.Category).filter(
        models.Category.name == cat_input.name
    ).first()
    if cat_db:
        raise HTTPException(400,detail='Category exists')
    cat_db = models.Category(
        name = cat_input.name,
        description = cat_input.description,
    )
    db.add(cat_db)
    db.commit()
    return cat_db

@router.put('/{category_id}',response_model=pyd.CategoryCreate)
async def change_category(cat_input:pyd.CategoryCreate,category_id:int,username=Depends(auth_handler.auth_wrapper),db:Session = Depends(get_db)):
    user_db = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if user_db.role_id == 1:
        raise HTTPException(401,'Нет прав')
    
    cat_db = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()
    if not cat_db:
        raise HTTPException(404,detail='Category not found')
    cat_db.name = cat_input.name
    cat_db.description = cat_input.description
    db.commit()
    return cat_db
    
@router.delete('/delete/{category_id}')
async def delete_category(category_id:int,username = Depends(auth_handler.auth_wrapper),db:Session=Depends(get_db)):
    user_db = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if user_db.role_id == 1:
        raise HTTPException(401,'Нет прав')
    
    cat_db = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()
    if not cat_db:
        raise HTTPException(403,detail='Category not found')
    db.delete(cat_db)
    db.commit()
    return 'success'
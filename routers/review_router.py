from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
from auth import AuthHandler

auth_handler = AuthHandler()

router = APIRouter(
    prefix="/review",
    tags=["review"],
)

@router.get('/',response_model=List[pyd.ReviewSchema])
async def get_reviews(db:Session=Depends(get_db)):
    rev_db = db.query(models.Review).all()
    return rev_db

@router.post('/add_review',response_model=pyd.ReviewCreate)
async def add_review(rev_input:pyd.ReviewCreate,username=Depends(auth_handler.auth_wrapper), db:Session=Depends(get_db)):
    user_db = db.query(models.User).filter(
        models.User.username == username
    ).first()

    prod_db = db.query(models.Product).filter(
        models.Product.id == rev_input.product_id
    ).first()

    if not prod_db:
        raise HTTPException(404,'Product not found')
    avg_rate = []

    rev_db = models.Review(
        body= rev_input.body,
        rating = rev_input.rating,
        user_id = user_db.id,
        product_id = rev_input.product_id
    )

    db.add(rev_db)
    db.commit()
    reviews_db = db.query(models.Review).filter(
        models.Review.product_id == rev_input.product_id
    ).all()
    for i in range(len(reviews_db)):
        avg_rate.append(reviews_db[i].rating)

    prod_db.avg_rating = round(sum(avg_rate)/len(reviews_db),2)
    db.commit()
    return rev_db

@router.put('/{review_id}',response_model=pyd.ReviewCreate)
async def change_review(rev_input:pyd.ReviewCreate,review_id:int,username=Depends(auth_handler.auth_wrapper),db:Session = Depends(get_db)):
    rev_db = db.query(models.Review).filter(
        models.Review.id == review_id
    ).first()
    if not rev_db:
        raise HTTPException(404,detail='Review not found')
    
    user_db = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if rev_db.user_id != user_db.id:
        raise HTTPException(401,"Не изменить...")

    rev_db.body = rev_input.body
    rev_db.rating = rev_input.rating
    avg_rate = []
    db.commit()
    reviews_db = db.query(models.Review).filter(
        models.Review.product_id == rev_input.product_id
    ).all()

    for i in range(len(reviews_db)):
        avg_rate.append(reviews_db[i].rating)

    prod_db = db.query(models.Product).filter(
        models.Product.id == rev_input.product_id
    ).first()

    if not prod_db:
        raise HTTPException(404,'Product not found')

    prod_db.avg_rating = round(sum(avg_rate)/len(reviews_db),2)
    db.commit()
    return rev_db
    
@router.delete('/delete/{review_id}')
async def delete_review(review_id:int,username = Depends(auth_handler.auth_wrapper),db:Session=Depends(get_db)):
    user_db = db.query(models.User).filter(
        models.User.username == username
    ).first()
    
    rev_db = db.query(models.Review).filter(
        models.Review.id == review_id
    ).first()
    if not rev_db:
        raise HTTPException(403,detail='Review not found')
    
    user_db = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if (rev_db.user_id != user_db.id):
        print(rev_db.user_id)
        print(user_db.id)
        print(user_db.role_id)
        if user_db.role_id !=1:
            db.delete(rev_db)
            db.commit()
            return 'success'
        raise HTTPException(401,"Не удалить...")
    
    rev_db = db.query(models.Review).filter(
        models.Review.id == review_id
    ).first()
    if not rev_db:
        raise HTTPException(404,detail='Review not found')

    db.delete(rev_db)
    db.commit()
    avg_rate = []
    reviews_db = db.query(models.Review).filter(
        models.Review.product_id == rev_db.product_id
    ).all()

    for i in range(len(reviews_db)):
        avg_rate.append(reviews_db[i].rating)

    prod_db = db.query(models.Product).filter(
        models.Product.id == rev_db.product_id
    ).first()

    if not prod_db:
        raise HTTPException(404,'Product not found')
    if len(reviews_db) >0:
        prod_db.avg_rating = round(sum(avg_rate)/len(reviews_db),2)
    elif len(reviews_db) == 0:
        prod_db.avg_rating = 0
    db.commit()
    return 'success'
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
from auth import AuthHandler

router = APIRouter(
    prefix="/user",
    tags=["users"],
)

auth_handler = AuthHandler()

@router.get('/',response_model=List[pyd.UserSchema])
async def get_reviews(db:Session=Depends(get_db)):
    rev_db = db.query(models.User).all()
    return rev_db

@router.post('/register',response_model=pyd.UserCreate)
async def user_reg(user_input:pyd.UserCreate,db:Session=Depends(get_db)):
    user_db = db.query(models.User).filter(
        models.User.username == user_input.username
    ).first()
    if user_db:
        raise HTTPException(400,'User exists')
    hashed_pass = auth_handler.get_password_hash(user_input.password)
    user_db = models.User(
        username = user_input.username,
        password = hashed_pass,
        role_id = user_input.role_id
    )
    db.add(user_db)
    db.commit()
    return user_db

@router.post('/login')
async def user_login(user_input:pyd.UserCreate,db:Session=Depends(get_db)):
    user_db = db.query(models.User).filter(
        models.User.username == user_input.username
    ).first()
    if not user_db:
        raise HTTPException(404,'User not found')
    if auth_handler.verify_password(user_input.password, user_db.password):
        token = auth_handler.encode_token(user_db.username)
        return {'token': token}
    else:
        raise HTTPException(403, 'xd')
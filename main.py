from fastapi import FastAPI
import models
from database import SessionLocal, engine
from routers import category_router, product_router, user_router, review_router

app = FastAPI()

app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(review_router)

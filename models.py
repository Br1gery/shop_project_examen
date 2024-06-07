from sqlalchemy import Numeric, Table, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


product_category = Table('product_category', Base.metadata,
                         Column('product_id', ForeignKey('products.id'), primary_key=True),
                         Column('category_id', ForeignKey('categories.id'), primary_key=True)
                         )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255), nullable=True)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255), nullable=True)
    price = Column(Integer, default=0)

    avg_rating = Column(Integer, default=0)

    categories = relationship("Category", secondary="product_category", backref="products")


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    body = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'), default= 1)

    user = relationship('User', backref='reviews')
    product = relationship('Product',backref='reviews')


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    
    role_id = Column(Integer,ForeignKey('roles.id'))

    role = relationship('Role', backref='users')

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String)
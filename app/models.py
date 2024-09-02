from . import db
from sqlalchemy import Column, Integer, String, Float

class Product(db.Model):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    category = Column(String)
    price = Column(Float)
    quantity_sold = Column(Integer)
    rating = Column(Float)
    review_count = Column(Integer)

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

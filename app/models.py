from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    month = Column(Integer)
    year = Column(Integer)
    amount = Column(Numeric)
    category = relationship("Category")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    amount = Column(Numeric, nullable=False)
    note = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = relationship("Category")

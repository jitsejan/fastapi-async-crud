from sqlalchemy import Column, DateTime, Integer, MetaData, String, func, Table
from .db import Base

metadata = MetaData()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    author = Column(String(50))
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())

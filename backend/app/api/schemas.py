from pydantic import BaseModel, Field
from typing import List


class Author(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    authors: List[Author]


class Book(BookBase):
    id: int



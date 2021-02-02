from pydantic import BaseModel, Field
from typing import List


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class Author(AuthorBase):
    id: int

class PublisherBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class Publisher(PublisherBase):
    id: int

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    authors: List[Author]
    publisher: Publisher


class Book(BookBase):
    id: int

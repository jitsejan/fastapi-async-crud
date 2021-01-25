from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    author: str = Field(..., min_length=1, max_length=50)


class Book(BookBase):
    id: int

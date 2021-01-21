from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    author: str = Field(..., min_length=1, max_length=50)


class BookDB(BookSchema):
    id: int

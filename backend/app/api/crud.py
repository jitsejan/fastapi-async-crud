from datetime import datetime
import sqlalchemy as sa

from app.api.schemas import BookBase
from app.db import database
from app.models import Book


async def post(payload: BookBase):
    values = {
        'title': payload.title,
    }
    query = sa.insert(Book)
    for author in payload.authors:
        print(author)

    book_id = await database.execute(query=query, values=values)
    return book_id


async def get(id: int):
    query = sa.select([Book]).where(id == Book.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = sa.select([Book])
    return await database.fetch_all(query=query)


async def put(id: int, payload: BookBase):
    values = {
        'title': payload.title,
        'author': payload.author,
    }
    query = (
        sa.update(Book)
        .where(id == Book.id)
        .returning(Book.id)
    )
    return await database.execute(query=query, values=values)


async def delete(id: int):
    query = sa.delete(Book).where(id == Book.id)
    return await database.execute(query=query)

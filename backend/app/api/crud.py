from app.api.schemas import BookBase
from app.db import database
from app.models import books


async def post(payload: BookBase):
    query = books.insert().values(title=payload.title, author=payload.author)
    return await database.execute(query=query)


async def get(id: int):
    query = books.select().where(id == books.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = books.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: BookBase):
    query = (
        books.update()
        .where(id == books.c.id)
        .values(title=payload.title, author=payload.author)
        .returning(books.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = books.delete().where(id == books.c.id)
    return await database.execute(query=query)

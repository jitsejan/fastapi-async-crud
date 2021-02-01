from datetime import datetime
import sqlalchemy as sa

from app.api.schemas import BookBase
from app.db import database
from app.models import Book, Author, AuthorBook


async def post(payload: BookBase):
    book_id = await database.execute(query=sa.insert(Book), values={'title': payload.title})
    for author in payload.authors:
        author_id = await database.execute(query=sa.insert(Author), values={'name': author.name})
        author_book = await database.execute(query=sa.insert(AuthorBook), values={'book_id': book_id, 'author_id': author_id})
    return book_id


async def get(id: int):
    query = sa.select([Book]).where(id == Book.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = sa.select([Book, Author])
    return await database.fetch_all(query=query)
    # print(results)
    # for result in results:
    #     print(dir(result))
    #     for key in result.keys():
    #         print(key)

        

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

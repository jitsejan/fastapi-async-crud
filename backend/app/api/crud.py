from datetime import datetime
from sqlalchemy.orm import Session
from app.api.schemas import BookBase
from app.db import database
from app.models import Book, Author, AuthorBook


# def post(payload: BookBase):
#     book_id = await database.execute(query=sa.insert(Book), values={'title': payload.title})
#     for author in payload.authors:
#         author_id = await database.execute(query=sa.insert(Author), values={'name': author.name})
#         author_book = await database.execute(query=sa.insert(AuthorBook), values={'book_id': book_id, 'author_id': author_id})
#     return book_id


def get(db: Session, id: int):
    return db.query(Book).filter(Book.id == id).first()

def get_all(db: Session):
    return db.query(Book).all()        

# def put(id: int, payload: BookBase):
#     values = {
#         'title': payload.title,
#         'author': payload.author,
#     }
#     query = (
#         sa.update(Book)
#         .where(id == Book.id)
#         .returning(Book.id)
#     )
#     return await database.execute(query=query, values=values)


def delete(db: Session, id: id):
    book = get(db, id)
    db.delete(book)
    db.commit()
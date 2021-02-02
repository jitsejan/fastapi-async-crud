from datetime import datetime
from sqlalchemy.orm import Session
from app.api.schemas import BookBase
from app.db import database
from app.models import Book, Author, AuthorBook, Publisher


def post(db: Session, payload: BookBase):
    publisher = Publisher(name=payload.publisher.name)
    book = Book(title=payload.title,
                publisher=publisher)
    db.add(book)
    db.flush()
    authors_db = [Author(name=author.name) for author in payload.authors]
    book.add_authors(authors_db)
    db.commit()
    return book.id


def get(db: Session, id: int):
    return db.query(Book).filter(Book.id == id).first()

def get_all(db: Session):
    return db.query(Book).all()        

def put(id: int, payload: Book):
    print(payload)
    values = {
        'title': payload.title,
        'authors': payload.authors,
    }
    # query = (
    #     sa.update(Book)
    #     .where(id == Book.id)
    #     .returning(Book.id)
    # )
    # return await database.execute(query=query, values=values)


def delete(db: Session, id: id):
    book = get(db, id)
    db.delete(book)
    db.commit()
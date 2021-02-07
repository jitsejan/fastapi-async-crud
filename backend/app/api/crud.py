from datetime import datetime
from sqlalchemy.orm import Session
from app.api.schemas import BookBase
from app.db import database
from app.models import Book, Author, AuthorBook, Publisher


def post(session: Session, payload: BookBase):
    publisher = Publisher(name=payload.publisher.name)
    book = Book(title=payload.title,
                publisher=publisher)
    session.add(book)
    session.flush()
    authors_db = [Author(name=author.name) for author in payload.authors]
    book.add_authors(authors_db)
    session.commit()
    return book.id


def get(session: Session, id: int):
    return session.query(Book).filter(Book.id == id).first()

def get_author_by_name(session: Session, name: str):
    return session.query(Author).filter(Author.name == name).first()

def get_publisher_by_name(session: Session, name: str):
    return session.query(Publisher).filter(Publisher.name == name).first()

def get_all(session: Session):
    return session.query(Book).all()        

def put(id: int, payload: BookBase):
    print("payload", payload)
    values = {
        'title': payload.title,
        'authors': payload.authors,
    }

    # query = (
    #     sa.update(Book)
    #     .where(id == Book.id)
    #     .returning(Book.id)
    # )
    return id


def delete(session: Session, id: id):
    book = get(session, id)
    session.delete(book)
    session.commit()
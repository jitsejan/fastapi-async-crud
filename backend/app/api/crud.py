from datetime import datetime
from sqlalchemy.orm import Session
from app.api.schemas import BookBase
from app.db import database
from app.models import Book, Author, AuthorBook, Publisher


def post_book(session: Session, payload: BookBase):
    publisher = get_publisher_by_name(session=session, name=payload.publisher.name)
    if publisher is None:
        publisher = Publisher(name=payload.publisher.name)
    book = Book(title=payload.title, publisher=publisher)
    authors = []
    for a in payload.authors:
        author = get_author_by_name(session=session, name=a.name)
        if author is None:
            author = Author(name=a.name)
        authors.append(author)
    book.add_authors(authors)
    session.add(book)
    session.commit()
    return book.id

def get_book_by_id(session: Session, id: int):
    return session.query(Book).filter(Book.id == id).first()

def get_author_by_name(session: Session, name: str):
    return session.query(Author).filter(Author.name == name).first()

def get_publisher_by_name(session: Session, name: str):
    return session.query(Publisher).filter(Publisher.name == name).first()

def get_all_books(session: Session):
    return session.query(Book).all()        

def put_book(session: Session, id: int, payload: BookBase):
    print("crud.put_book")
    print("payload", payload)
    values = {
        'title': payload.title,
        'authors': payload.authors,
    }

    query = session.query(Book).update(values).where(id == Book.id).returning(Book.id)
    
    return id


def delete_book_by_id(session: Session, id: id):
    book = get(session, id)
    session.delete(book)
    session.commit()
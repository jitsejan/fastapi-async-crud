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

def put_book(session: Session, id: int, payload: BookBase, book: Book):
    new_authors = [y for y in payload.authors if y.id not in [x.id for x in book.authors]]
    authors = []
    for a in new_authors:
        author = get_author_by_name(session=session, name=a.name)
        if author is None:
            author = Author(name=a.name)
        authors.append(author)
    book.add_authors(authors)

    deleted_authors = [y for y in book.authors if y.id not in [x.id for x in payload.authors]]
    for a in deleted_authors:
        author = get_author_by_name(session=session, name=a.name)
        book.authors.remove(author)
    
    changed_authors = [y for y in payload.authors if y.id in [x.id for x in book.authors]]
    for a in changed_authors:
        author = session.query(Author).filter(Author.id == a.id).one()
        author.name = a.name
    
    session.add(book)
    session.commit()
    
    return id


def delete_book_by_id(session: Session, id: id):
    book = get_book_by_id(session, id)
    session.delete(book)
    session.commit()
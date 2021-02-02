from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Table,
                        func)
from sqlalchemy.orm import backref, relationship
import yaml
from .db import Base


class AuthorBook(Base):
    __tablename__ = 'assoc_author_book'
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'), primary_key=True)

    book = relationship("Book", backref=backref("assoc_author_book", cascade="all, delete-orphan" ))
    author = relationship("Author", backref=backref("assoc_author_book", cascade="all, delete-orphan" ))

    def __init__(self, author=None, book=None):
        self.author = author
        self.book =  book

    def __repr__(self):
        return f"<AuthorBook {self.author.name} {self.book.title}>"


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(80), nullable=False)
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    books = relationship("Book", secondary="assoc_author_book")

    def __init__(self, name):
        self.name = name
        self.books =[]

    def __repr__(self):
        return f"<Author {self.name}>"

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(80), nullable=False)
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())
    publisher_id = Column(Integer, ForeignKey("publishers.id"))
    authors = relationship("Author", secondary="assoc_author_book")

    def __init__(self, title, publisher):
        self.title = title
        self.publisher = publisher
        self.authors = []

    def __repr__(self):
        return f"<Book {self.title}>"
    
    def add_authors(self, items):
        for author in items:
            self.assoc_author_book.append(AuthorBook(book=self, author=author))

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "publisher": self.publisher.as_dict(),
            "authors": [a.as_dict() for a in self.authors]
        }
 

class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(80), nullable=False)
    books = relationship("Book", backref=backref("publisher"))
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Publisher {self.name}>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

def load_data():
    with open(r'books.yaml') as file:
        documents = yaml.full_load(file)

        for item, doc in documents.items():
            print(item, ":", doc)
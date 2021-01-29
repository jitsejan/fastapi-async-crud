from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Table,
                        func)
from sqlalchemy.orm import backref, relationship

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

    books = relationship("Book", secondary="assoc_author_book", viewonly=True)

    def __init__(self, name):
        self.name = name
        self.books =[]

    def __repr__(self):
        return f"<Book {self.name}>"


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(80), nullable=False)

    authors = relationship("Author", secondary="assoc_author_book", viewonly=True)

    def __init__(self, title):
        self.title = title
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
            "authors": [a.name for a in self.authors]
        }
 
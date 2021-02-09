from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path

from app.api import crud
from app.db import get_db
from app.api.schemas import Book, BookBase

router = APIRouter()


@router.post("/", response_model=BookBase, status_code=201)
def create_book(payload: BookBase, session: Session = Depends(get_db)):
    book_id = crud.post_book(session=session, payload=payload)
    response_object = {
        "id": book_id,
        "title": payload.title,
        "publisher": payload.publisher,
        "authors": payload.authors
    }
    return response_object


@router.get("/{id}/", response_model=Book)
def read_book(
    session: Session = Depends(get_db),
    id: int = Path(..., gt=0)
):
    book = crud.get_book_by_id(db, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.as_dict()


@router.get("/", response_model=List[Book])
def read_all_books(session: Session = Depends(get_db)):
    result = []
    for book in crud.get_all_books(session=session):
        result.append(book.as_dict())
    return result


@router.put("/{id}/", response_model=Book)
def update_book(
    payload: BookBase,
    id: int = Path(..., gt=0),
    session: Session = Depends(get_db)
):
    print("PP>")
    print(payload)
    book = crud.get_book_by_id(session=session, id=id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book_id = crud.put_book(session, id, payload)
    for a in payload.authors:
        author = crud.get_author_by_name(session=session, name=a)
        print(author)
    response_object = {
        "id": book_id,
        "title": payload.title,
        "authors": payload.authors,
        "publisher": payload.publisher
    }
    return response_object


@router.delete("/{id}/")
def delete_book(session: Session = Depends(get_db), id: int = Path(..., gt=0)):
    book = crud.get_book_by_id(session=session, id=id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    crud.delete_book_by_id(session=session, id=id)

    return {}

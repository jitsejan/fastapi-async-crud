from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path

from app.api import crud
from app.db import get_db
from app.api.schemas import Book, BookBase

router = APIRouter()


@router.post("/", response_model=Book, status_code=201)
def create_book(payload: BookBase):
    print(payload)
    book_id = crud.post(payload)

    response_object = {
        "id": book_id,
        "title": payload.title,
        "authors": payload.authors,
        "publisher": payload.publisher
    }
    return response_object


@router.get("/{id}/", response_model=Book)
def read_book(
    db: Session = Depends(get_db),
    id: int = Path(..., gt=0)
):
    book = crud.get(db, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.as_dict()


@router.get("/", response_model=List[Book])
def read_all_books(db: Session = Depends(get_db)):
    result = []
    for book in crud.get_all(db):
        result.append(book.as_dict())
    return result


@router.put("/{id}/", response_model=Book)
def update_book(
    payload: BookBase,
    id: int = Path(..., gt=0),
):
    book = crud.get(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book_id = crud.put(id, payload)

    response_object = {
        "id": book_id,
        "title": payload.title,
        "authors": payload.authors,
        "publisher": payload.publisher
    }
    return response_object


@router.delete("/{id}/")
def delete_book(db: Session = Depends(get_db), id: int = Path(..., gt=0)):
    book = crud.get(db, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    crud.delete(db, id)

    return {}

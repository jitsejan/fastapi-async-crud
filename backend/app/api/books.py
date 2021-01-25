from typing import List

from app.api import crud
from app.api.schemas import Book, BookBase
from fastapi import APIRouter, HTTPException, Path

router = APIRouter()


@router.post("/", response_model=Book, status_code=201)
async def create_book(payload: BookBase):
    book_id = await crud.post(payload)

    response_object = {
        "id": book_id,
        "title": payload.title,
        "author": payload.author,
    }
    return response_object


@router.get("/{id}/", response_model=Book)
async def read_book(
    id: int = Path(..., gt=0),
):
    book = await crud.get(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/", response_model=List[Book])
async def read_all_books():
    return await crud.get_all()


@router.put("/{id}/", response_model=Book)
async def update_book(
    payload: BookBase,
    id: int = Path(..., gt=0),
):
    book = await crud.get(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book_id = await crud.put(id, payload)

    response_object = {
        "id": book_id,
        "title": payload.title,
        "author": payload.author,
    }
    return response_object


@router.delete("/{id}/", response_model=Book)
async def delete_book(id: int = Path(..., gt=0)):
    book = await crud.get(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await crud.delete(id)

    return book

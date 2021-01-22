from app.api import crud
from app.api.models import BookDB, BookSchema
from fastapi import APIRouter, HTTPException, Path
from typing import List

router = APIRouter()


@router.post("/", response_model=BookDB, status_code=201)
async def create_book(payload: BookSchema):
    book_id = await crud.post(payload)

    response_object = {
        "id": book_id,
        "title": payload.title,
        "author": payload.author,
    }
    return response_object


@router.get("/{id}/", response_model=BookDB)
async def read_book(
    id: int = Path(..., gt=0),
):
    book = await crud.get(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/", response_model=List[BookDB])
async def read_all_books():
    return await crud.get_all()


@router.put("/{id}/", response_model=BookDB)
async def update_book(
    payload: BookSchema,
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


@router.delete("/{id}/", response_model=BookDB)
async def delete_book(id: int = Path(..., gt=0)):
    book = await crud.get(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await crud.delete(id)

    return book

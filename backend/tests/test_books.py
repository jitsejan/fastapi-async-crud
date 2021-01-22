import json

import pytest
from app.api import crud


def test_create_book(test_app, monkeypatch):
    test_request_payload = {"title": "Test Title", "author": "Fake author"}
    test_response_payload = {"id": 1, "title": "Test Title", "author": "Fake author"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(
        "/books/",
        data=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "payload, status_code",
    [
        [{"title": "", "author": "Fake author"}, 422],
        [{"title": "Fake title", "author": ""}, 422],
        [{"title": "", "author": ""}, 422],
    ],
    ids=["empty-title", "empty-author", "both-empty"],
)
def test_create_books_invalid_json_missing_author(test_app, payload, status_code):
    response = test_app.post("/books/", data=json.dumps(payload))
    assert response.status_code == status_code


def test_read_book(test_app, monkeypatch):
    test_data = {"id": 1, "title": "Test Title", "author": "Fake author"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/books/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_book_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/books/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_read_all_books(test_app, monkeypatch):
    test_data = [
        {"id": 1, "title": "Test Title", "author": "Fake author"},
        {"id": 2, "title": "Test Another Title", "author": "Fake writer"},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/books/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_book(test_app, monkeypatch):
    test_update_data = {"title": "Test Title", "author": "Real author", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/books/1/", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"title": "Fake title"}, 422],
        [999, {"title": "Fake title", "author": "Fake author"}, 404],
        [1, {"title": "Fake title", "author": ""}, 422],
        [1, {"title": "", "author": "Fake author"}, 422],
        [0, {"title": "", "author": ""}, 422],
    ],
    ids=[
        "empty-payload",
        "missing-author",
        "invalid-id",
        "empty-author",
        "empty-title",
        "both-empty",
    ],
)
def test_update_book_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(
        f"/books/{id}/",
        data=json.dumps(payload),
    )
    assert response.status_code == status_code


def test_remove_book(test_app, monkeypatch):
    test_data = {"title": "Fake title", "author": "Fake author", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/books/1/")
    assert response.status_code == 200
    assert response.json() == test_data


@pytest.mark.parametrize(
    "id, status_code, detail",
    [
        [999, 404, "Book not found"],
        [
            0,
            422,
            [
                {
                    "loc": ["path", "id"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 0},
                }
            ],
        ],
    ],
    ids=["non-existing-id", "wrong-id"],
)
def test_remove_book_incorrect_id(test_app, monkeypatch, id, status_code, detail):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete(f"/books/{id}/")

    assert response.status_code == status_code
    assert response.json()["detail"] == detail

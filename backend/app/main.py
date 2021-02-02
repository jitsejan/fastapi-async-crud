from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import books, healthcheck
from app.db import database, engine
from app.models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI()
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(healthcheck.router)
app.include_router(books.router, prefix="/books", tags=["books"])

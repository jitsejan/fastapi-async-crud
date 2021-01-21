import os

from databases import Database
from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.sql import func

host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
username = os.environ["POSTGRES_API_USER"]
password = os.environ["POSTGRES_API_PASS"]
database = os.environ["POSTGRES_API_DB"]

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)
metadata = MetaData()
books = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("author", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

database = Database(DATABASE_URL)
import os

from databases import Database
from sqlalchemy import (Column, DateTime, Integer, String, Table,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
username = os.environ["POSTGRES_API_USER"]
password = os.environ["POSTGRES_API_PASS"]
database = os.environ["POSTGRES_API_DB"]

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)
Base = declarative_base()

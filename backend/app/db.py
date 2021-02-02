import os

from sqlalchemy import Column, DateTime, Integer, String, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
username = os.environ["POSTGRES_API_USER"]
password = os.environ["POSTGRES_API_PASS"]
database = os.environ["POSTGRES_API_DB"]

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
